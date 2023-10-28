# Purpose: Prints the number of characters and words in each chapter of a book.
# Author: Gary A. Stafford
# Date: 2023-10-28

import datetime
import logging.config
from statistics import mean
import string

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

    logger.info(f"Start time: {datetime.datetime.now()}")
    chapter_lengths = []
    word_count = []

    for i, chapter in enumerate(chapters):
        try:
            chapter_length_tmp = len(chapter.strip())
            # print(chapter_length_tmp)
            chapter_lengths.append(chapter_length_tmp)

            # https://www.geeksforgeeks.org/python-program-to-count-words-in-a-sentence/
            word_count_tmp = sum(
                [i.strip(string.punctuation).isalpha() for i in chapter.split()]
            )
            word_count.append(word_count_tmp)
            # print(word_count_tmp)
            # print("\n")
            # print(len(chapter.split(" ")))

            print(f"Chapter: {i+1}\t{chapter_length_tmp}\t{word_count_tmp}")

        except Exception as ex:
            logger.error(ex)

    print(f"chapters: {len(chapters)}")
    print(f"min chars: {min(chapter_lengths)}")
    print(f"max chars: {max(chapter_lengths)}")
    print(f"mean chars: {int(mean(chapter_lengths))}")
    print(f"count chars: {int(sum(chapter_lengths))}")

    print(f"min words: {min(word_count)}")
    print(f"max words: {max(word_count)}")
    print(f"mean words: {int(mean(word_count))}")
    print(f"count words: {int(sum(word_count))}")

    logger.info(f"Finish time: {datetime.datetime.now()}")


if __name__ == "__main__":
    main()
