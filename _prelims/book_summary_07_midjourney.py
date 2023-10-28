import logging.config

from utilities import Utilities

logger = logging.getLogger(__name__)
logging.config.fileConfig("logging.ini", disable_existing_loggers=False)


def main():
    utilities = Utilities("anthropic.claude-v2", 500, 0.3, 250, 0.999, ["\n\nHuman:"])

    client_bedrock = utilities.create_bedrock_connection()

    file_path = "../output/dracula_summary_03.txt"

    # Open the file in read mode and read its contents into a string
    with open(file_path, "r") as file:
        character_summary = file.read()

    prompt = """### INSTRUCTIONS ###
        Using the summaries of chapters, below, write a concise Midjourney-style prompt for text-to-image generation.
        ### SUMMARIES ###"""

    try:
        summary = utilities.create_summary(client_bedrock, character_summary, prompt)
    except Exception as ex:
        logger.error(ex)
        exit(0)

    with open(f"../output/midjourney_summary.txt", "w") as f:
        f.write(summary)


if __name__ == "__main__":
    main()
