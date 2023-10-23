import datetime
import json
import logging
import re
import sys

import boto3
from botocore.exceptions import ClientError

BEDROCK_MODEL_SUMMARIZATION = "anthropic.claude-v2"

# logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# terminal logger
stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


# split the book into chapters
def split_book(book_text):
    # Use regular expressions to split the book by chapter
    chapters = re.split(r"^CHAPTER [IVXLCDM]+$", book_text, flags=re.MULTILINE)
    chapters.pop(0)

    # Split the last chapter into two parts and remove everything after "THE END"
    chapter26 = re.split(r"^.*THE END.*$", chapters[26], flags=re.MULTILINE)[0]
    chapters.pop(26)
    chapters.append(chapter26)

    return chapters


# create bedrock client connection
def create_bedrock_connection():
    # boto3.set_stream_logger("", logging.ERROR)
    client_bedrock = boto3.client("bedrock-runtime", "us-east-1")

    return client_bedrock


# create a summary of a single chapter
def create_summary(client_bedrock, chapter):
    prompt = "Summerize the main highlights from the following chapter using bulleted text:"

    body = json.dumps(
        {
            "prompt": f"\n\nHuman:{prompt}\n\n{chapter}\n\nAssistant:",
            "max_tokens_to_sample": 300,
            # "temperature": 0.3,
            # "top_k": 250,
            # "top_p": 0.999,
            "stop_sequences": ["\n\nHuman:"],
        }
    )
    logger.debug(body)

    model_id = BEDROCK_MODEL_SUMMARIZATION
    accept = "application/json"
    content_type = "application/json"

    response = client_bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    logger.debug(f"{BEDROCK_MODEL_SUMMARIZATION} called...")
    return response_body.get("completion").strip()
    # return response_body.get("completion").split("\n", 2)[2].strip()


def main():
    # Specify the path to the text file you want to read
    # https://www.gutenberg.org/cache/epub/345/pg345-images.html
    file_path = "./dracula.txt"

    # Open the file in read mode and read its contents into a string
    with open(file_path, "r") as file:
        book_text = file.read()

    chapters = split_book(book_text)

    client_bedrock = create_bedrock_connection()

    summary = ""

    logger.info(f"Start time: {datetime.datetime.now()}")

    for i, chapter in enumerate(chapters):
        try:
            chapter_summary = create_summary(client_bedrock, chapter)
            logger.info(f"Chapter {i + 1} summary ")
        except ClientError as ex:
            logger.error(ex)
            exit(0)
        except Exception as ex:
            logger.error(ex)
            chapter_summary = f"Chapter {i + 1} summary not available: {ex}"

        summary += f"\nChapter {i + 1}:\n{chapter_summary}\n\n"

    logger.info(f"Finish time: {datetime.datetime.now()}")

    with open("summary.txt", "w") as f:
        f.write(summary)


if __name__ == "__main__":
    main()
