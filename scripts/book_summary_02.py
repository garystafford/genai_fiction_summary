import datetime
import logging
import logging.config

from utilities import Utilities

logger = logging.getLogger(__name__)
logging.config.fileConfig("logging.ini", disable_existing_loggers=False)


def main():
    # specify the path to the text file you want to read
    # https://www.gutenberg.org/cache/epub/345/pg345-images.html
    file_path = "../input/dracula.txt"
    title = "Dracula"

    # Open the file in read mode and read its contents into a string
    with open(file_path, "r") as file:
        book_text = file.read()

    utilities = Utilities("anthropic.claude-v2")

    chapters = utilities.split_book(book_text)

    client_bedrock = utilities.create_bedrock_connection()

    summary = ""

    logger.info(f"Start time: {datetime.datetime.now()}")

    for i, chapter in enumerate(chapters):
        try:
            prompt = "Please provide a concise bullet-point summary of the main points, events, and ideas covered in following chapter:"
            chapter_summary = utilities.create_summary(client_bedrock, chapter, prompt)
            chapter_summary = f"\nChapter {i + 1}:\n{chapter_summary}\n\n"
            summary += chapter_summary
            logger.info(f"Chapter {i + 1} completed...")
        except Exception as ex:
            chapter_summary = f"Chapter {i + 1} summary failed: {ex}"
            logger.error(chapter_summary)
            summary += chapter_summary

    logger.info(f"Finish time: {datetime.datetime.now()}")

    with open(f"../output/{title.lower()}_summary_02.txt", "w") as f:
        f.write(summary)


if __name__ == "__main__":
    main()
