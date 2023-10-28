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
        chapter_summaries = file.read()

    prompt = f"""Write a concise one-paragraph summary of the main points, events, and ideas covered in following individual chapter summaries. 
        Construct a complete, grammatically-correct paragraph. DO NOT use bullet points. 

        <chapter_summaries>
        {chapter_summaries.strip()}
        </chapter_summaries>"""

    try:
        summary = utilities.create_summary(client_bedrock, chapter_summaries, prompt)
    except Exception as ex:
        logger.error(ex)
        exit(0)

    with open(f"../output/summary_of_summaries.txt", "w") as f:
        f.write(summary)


if __name__ == "__main__":
    main()
