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
            # prompt = "Generate a list of 3 hypothetical questions that the below chapter could be used to answer:"
    
            # simple question and answer
            prompt = f"""Generate a list of 3 hypothetical questions that the following chapter, contained in the <chapter> tags below, could be used to answer. 
                The Assistant will provide both the question and the answer.
                The Assistant will refrain from asking overly broad questions.
                The Assistant will refrain from using bullet-point lists.
                Follow the template contained in the <template> tags below and replace the placeholders with the relevant information:
                <template>
                Q: [Question]
                A: [Answer]
                <template>
                
                Here is an example contained in the <example> tags below:
                <example>
                Q: What is the weather like in Spain?
                A: The rain in Spain stays mainly in the plain.
                </example>
                
                <chapter>
                {chapter.strip()}
                </chapter>"""
    
            # multiple choice question and answer
            prompt = f"""Generate a list of 3 hypothetical multiple-choice questions that the following chapter, contained in the <chapter> tags below, could be used to answer. 
                The Assistant will provide the question, four possible answers, and the correct answer.
                The Assistant will ask brief, specific questions.
                The Assistant will refrain from using bullet-point lists.
                Follow the template contained in the <template> tags below and replace the placeholders with the relevant information:
                <template>
                Q: [Question]
                (a) [Choice 1]
                (b) [Choice 2]
                (c) [Choice 3]
                (d) [Choice 3]
                A: [Answer]
                <template>
                
                Here is an example contained in the <example> tags below:
                <example>
                Q: What color is fresh grass?
                (a) Red
                (b) Blue
                (c) Green
                (d) Yellow
                A: Green
                </example>
                
                <chapter>
                {chapter.strip()}
                </chapter>"""
        
            chapter_summary = utilities.create_summary(client_bedrock, chapter, prompt)
            chapter_summary = f"\nChapter {i + 1}:\n{chapter_summary}\n\n"
            summary += chapter_summary
            logger.info(f"Chapter {i + 1} completed...")
        except Exception as ex:
            chapter_summary = f"Chapter {i + 1} summary failed: {ex}"
            logger.error(chapter_summary)
            summary += chapter_summary

    logger.info(f"Finish time: {datetime.datetime.now()}")

    with open(f"../output/{title.lower()}_summary_04_multiple_choice.txt", "w") as f:
        f.write(summary)


if __name__ == "__main__":
    main()
