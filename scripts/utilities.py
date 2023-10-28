import json
import logging
import logging.config
import re

import boto3
from botocore.exceptions import ClientError


class Utilities:
    # constructor
    def __init__(
            self,
            model="anthropic.claude-v2",
            max_tokens_to_sample=500,
            temperature=0.3,
            top_k=250,
            top_p=0.999,
            stop_sequences=None
    ):
        if stop_sequences is None:
            stop_sequences = ["\n\nHuman:"]

        self.model = model
        self.max_tokens_to_sample = max_tokens_to_sample
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.stop_sequences = stop_sequences
        self.logger = logging.getLogger(__name__)
        logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

    # split the book into chapters
    def split_book(self, book_text):
        # Use regular expressions to split the book by chapter
        # Specific to this Gutenberg eBooks format
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
                    "max_tokens_to_sample": self.max_tokens_to_sample,
                    "temperature": self.temperature,
                    "top_k": self.top_k,
                    "top_p": self.top_p,
                    "stop_sequences": self.stop_sequences,
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
            formatted_response = (
                response_body.get("completion").split("\n", 2)[2].strip()
            )
            return formatted_response
        except ClientError as ex:
            self.logger.error(ex)
            exit(1)

    def count_tokens(self, client_bedrock, chapter):
        try:
            body = json.dumps(
                {
                    "prompt": f"\n\nHuman:{chapter.strip()}\n\nAssistant:",
                    "max_tokens_to_sample": self.max_tokens_to_sample,
                    "temperature": self.temperature,
                    "top_k": self.top_k,
                    "top_p": self.top_p,
                    "stop_sequences": self.stop_sequences,
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
            # self.logger.info(f"Response body: {response_body}")

            # remove the first line of text that explains the task completed
            # e.g. " Here are three hypothetical questions that the passage could help answer:\n\n"
            formatted_response = (
                response_body.get("completion").split("\n", 2)[2].strip()
            )
            return formatted_response
        except ClientError as ex:
            self.logger.error(ex)
            exit(1)

    def create_summary_full_prompt(self, client_bedrock, prompt):
        try:
            body = json.dumps(
                {
                    "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                    "max_tokens_to_sample": self.max_tokens_to_sample,
                    "temperature": self.temperature,
                    "top_k": self.top_k,
                    "top_p": self.top_p,
                    "stop_sequences": self.stop_sequences,
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
            formatted_response = (
                response_body.get("completion").split("\n", 2)[2].strip()
            )
            return formatted_response
        except ClientError as ex:
            self.logger.error(ex)
            exit(1)
