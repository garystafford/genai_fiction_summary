import logging.config

from utilities import Utilities

logger = logging.getLogger(__name__)
logging.config.fileConfig("logging.ini", disable_existing_loggers=False)


def main():
    utilities = Utilities("anthropic.claude-v2", 500, 0.3, 250, 0.999, ["\n\nHuman:"])

    client_bedrock = utilities.create_bedrock_connection()

    file_path = "../output/dracula_summary_05bv2.txt"

    # Open the file in read mode and read its contents into a string
    with open(file_path, "r") as file:
        character_summary = file.read()

    prompt = """### INSTRUCTIONS ###
        Using the summary below, write a one-paragraph description of the character, Dracula (aka Count Dracula):
        ### SUMMARY ###"""

    # prompt = """### INSTRUCTIONS ###
    #     Using the summary below, write a one-paragraph description of the main character, Jonathan Harker:
    #     ### SUMMARY ###"""

    try:
        summary = utilities.create_summary(client_bedrock, character_summary, prompt)
    except Exception as ex:
        logger.error(ex)
        exit(0)

    with open(f"../output/dracula_summary.txt", "w") as f:
        f.write(summary)


if __name__ == "__main__":
    main()
