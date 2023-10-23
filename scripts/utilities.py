import json
import logging
import re

import boto3
from botocore.exceptions import ClientError


class Utilities:
    # constructor
    def __init__(self, model):
        self.model = model
        self.logger = logging.getLogger(__name__)
        logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

    # split the book into chapters
    def split_book(self, book_text):
        # Use regular expressions to split the book by chapter
        # Specific to Gutenberg eBooks format
        chapters = re.split(r"^CHAPTER [IVXLCDM]+$", book_text, flags=re.MULTILINE)
        chapters.pop(0)

        # Split the last chapter into two parts and remove everything after "THE END"
        chapter26 = re.split(r"^.*THE END.*$", chapters[26], flags=re.MULTILINE)[0]
        chapters.pop(26)
        chapters.append(chapter26)

        return chapters

    # create bedrock client connection
    def create_bedrock_connection(self):
        client_bedrock = boto3.client("bedrock-runtime", "us-east-1")

        return client_bedrock

    # summarize a single chapter
    def create_summary(self, client_bedrock, chapter, prompt):
        try:
            body = json.dumps(
                {
                    "prompt": f"\n\nHuman:{prompt}\n\n{chapter.strip()}\n\nAssistant:",
                    "max_tokens_to_sample": 300,
                    "temperature": 0.0,
                    # "top_k": 250,
                    # "top_p": 0.999,
                    "stop_sequences": ["\n\nHuman:"],
                }
            )
            self.logger.debug(f"Request body: {body}")

            accept = "application/json"
            content_type = "application/json"

            response = client_bedrock.invoke_model(
                body=body, modelId=self.model, accept=accept, contentType=content_type
            )
            self.logger.debug(f"{self.model} called...")
            response_body = json.loads(response.get("body").read())
            self.logger.info(f"Response body: {response_body}")

            # remove the first line of text that explains the task completed
            # e.g. " Here are three hypothetical questions that the passage could help answer:\n\n"
            formatted_response = response_body.get("completion").split("\n", 2)[2].strip()
            return formatted_response
        except ClientError as ex:
            self.logger.error(ex)
            exit(0)
