# Purpose: Creates a list of settings for the chapters
# Author: Gary A. Stafford
# Date: 2023-10-28

import datetime
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

    utilities = Utilities("anthropic.claude-v2", 500, 0.3, 250, 0.999, ["\n\nHuman:"])

    chapters = utilities.split_book(book_text)

    client_bedrock = utilities.create_bedrock_connection()

    summary = ""
    start_time = f"Start time: {datetime.datetime.now()}"
    logger.info(start_time)
    summary += f"{start_time}\n"

    for i, chapter in enumerate(chapters):
        try:
            # prompt = "Provide a bullet-point brief description of each geographic location in the following chapter. Order the locations by how many times they are mentioned.  Start each description with the name of the location followed by a colon, not a dash."
            
            # prompt = "Provide a bullet-point brief description of physical locations in the following chapter. Start each description with the name of the location followed by a colon (':')."

            # prompt = "Provide a bullet-point brief description of geographic locations in the following chapter. Format each location as '{location}: {description}'."

            # prompt = """### INSTRUCTIONS ###
            #     Provide a bullet-point brief description of top three most-mentioned geographic locations in the following chapter.
            #     Here is an example: '- Hoboken, NJ: A New Jersey city on the Hudson River, containing many resturants and bars.
            #     Format each bullet-point like this: '- Location: Description'.
            #     ### CHAPTER ###"""

            prompt = f"""Provide a list of the no more than three settings and a brief description of each setting, in the chapter contained in the <chapter> tags below.
                The Assistant will order the settings by how many times they are mentioned in the chapter.
                The Assistant will number the list of settings.
                Follow the template contained in the <template> tags below and replace the placeholders with the relevant information:
                <template>
                [Number]. [Setting]: [Description]
                <template>

                Here is an example contained in the <example> tags below:
                <example>
                1. Hoboken, New Jersey: Part of the New York metropolitan area on the banks of the Hudson River across from lower Manhattan.
                </example>

                <chapter>
                {chapter.strip()}
                </chapter>"""

            chapter_summary = utilities.create_summary_full_prompt(
                client_bedrock, prompt
            )
            chapter_summary = f"\nChapter {i + 1}:\n{chapter_summary}\n\n"
            summary += chapter_summary
            logger.info(f"Chapter {i + 1} completed...")
        except Exception as ex:
            chapter_summary = f"Chapter {i + 1} summary failed: {ex}"
            logger.error(chapter_summary)
            summary += chapter_summary

    finish_time = f"Finish time: {datetime.datetime.now()}"
    logger.info(finish_time)
    summary += f"{finish_time}"

    with open(f"../output/{title.lower()}_summary_settings.txt", "w") as f:
        f.write(summary)


if __name__ == "__main__":
    main()
