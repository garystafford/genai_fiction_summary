# Purpose: Creates character descriptions of each chapter of a book.
# Author: Gary A. Stafford
# Date: 2023-10-28

import logging.config

from utilities import Utilities

logger = logging.getLogger(__name__)
logging.config.fileConfig("logging.ini", disable_existing_loggers=False)


def main():
    utilities = Utilities("anthropic.claude-v2", 500, 0.3, 250, 0.999, ["\n\nHuman:"])

    client_bedrock = utilities.create_bedrock_connection()

    file_path = "../output/dracula_summary_05b.txt"

    # Open the file in read mode and read its contents into a string
    with open(file_path, "r") as file:
        character_summaries = file.read()

    prompt = f"""Write a concise, grammatically correct, single-paragraph description of the main character, Dracula (aka Count Dracula), based on the following individual character descriptions. 
        The Assistant will refrain from using bullet-point lists.

        <summaries>
        {character_summaries}
        </summaries>"""
    try:
        summary = utilities.create_summary_full_prompt(client_bedrock, prompt)
    except Exception as ex:
        logger.error(ex)
        exit(0)

    with open(f"../output/dracula_summary_v2.txt", "w") as f:
        f.write(summary)


if __name__ == "__main__":
    main()
