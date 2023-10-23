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
            # summary 5a
            # prompt = "Provide a brief description of each character in the following chapter. Start each description with the name of the character followed by a colon, not a dash."
            
            # summary 5b
            # prompt = "Provide a bullet-point brief description of each character in the following chapter. Order the characters by how many times they are mentioned. Start each description with the name of the character followed by a colon, not a dash."
            
            # summary 5c
            # prompt = "Provide a bullet-point brief description of each geographic location in the following chapter. Order the locations by how many times they are mentioned.  Start each description with the name of the location followed by a colon, not a dash."
            # prompt = "Provide a bullet-point brief description of physical locations in the following chapter. Start each description with the name of the location followed by a colon (':')."
            
            # summary 5d
            # prompt = "Provide a bullet-point brief description of geographic locations in the following chapter. Format each location as '{location}: {description}'."

            # summary 5e
            # prompt = "Provide a bullet-point brief description of top three most-mentioned geographic locations in the following chapter. Format each location as '{location}: {description}'."

            # summary 5f
            prompt = """The following types of characters often found in fictional novels: 
                - Protagonist
                - Antihero
                - Antagonist
                - Guide
                - Contagonist
                - Sidekicks (Deuteragonist)
                - Henchmen
                - Love Interest
                - Temptress
                - Confidant
                - Foil

                Given the above is of character types, identify characters in the following chapter that fit these types. Only use these roles.
                If no character fits a type, igore it. Format each character as '{character name} - {type}: {description}'.
            """

            # summary 5g
            # prompt = "Provide a bullet-point list of three words or short phrases that best describe the following chapter."
            prompt = "Provide a bullet-point list of three words that best describe the following chapter and give the reason why. Format each location as '{the word}: {reason why}'."

            chapter_summary = utilities.create_summary(client_bedrock, chapter, prompt)
            chapter_summary = f"\nChapter {i + 1}:\n{chapter_summary}\n\n"
            summary += chapter_summary
            logger.info(f"Chapter {i + 1} completed...")
        except Exception as ex:
            chapter_summary = f"Chapter {i + 1} summary failed: {ex}"
            logger.error(chapter_summary)
            summary += chapter_summary

    logger.info(f"Finish time: {datetime.datetime.now()}")

    with open(f"../output/{title.lower()}_summary_05g.txt", "w") as f:
        f.write(summary)


if __name__ == "__main__":
    main()