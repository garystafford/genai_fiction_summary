# Purpose: Creates a character types summary of each chapter of a book.
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
            # summary 5a
            # prompt = "Provide a brief description of each character in the following chapter. Start each description with the name of the character followed by a colon, not a dash."

            # # summary 5b1
            # prompt = """### INSTRUCTIONS ###
            #     Provide a bullet-point brief description of each character in the following chapter. Order the characters by how many times they are mentioned.
            #     Here is an example: '- Pink Panther: A fictional animated character who is a suave and smooth-talking anthropomorphic panther.
            #     Format each character like this: '- Character name: Description'.
            #     ### CHAPTER ###"""

            # # summary 5b2
            # prompt = """### INSTRUCTIONS ###
            #     Provide a bullet-point list of main characters and a brief description of each main character in the following chapter.
            #     Follow the template below and fill in the information accordingly:
            #     -[Character_Name]: [Description]
            #     Here is an example: '- Pink Panther: A suave and smooth-talking anthropomorphic animated panther.
            #     ### CHAPTER ###"""

            # summary 5b3
            # prompt = """### INSTRUCTIONS ###
            #     Provide a list of the 3-4 main characters and a brief description of each main character, in the following chapter.
            #     Follow the template below and fill in the information accordingly. Replace the placeholders with the relevant information: [Character_Name]: [Description]
            #     Here is an example: 'Pink Panther: A suave and smooth-talking anthropomorphic animated panther.'
            #     ### CHAPTER ###"""

            # summary 5b3
            # prompt = f"""Provide a list of the 3-4 main characters and a brief description of each main character, in the chapter contained in the <chapter> tags below.
            #     The Assistant will order the main characters by how many times they are mentioned.
            #     The Assistant will number the characters.
            #     Follow the template contained in the <template> tags below and replace the placeholders with the relevant information:
            #     <template>
            #     [Number]. [Character]: [Description]
            #     <template>

            #     Here is an example contained in the <example> tags below:
            #     <example>
            #     1. Pink Panther: A suave and smooth-talking anthropomorphic animated panther.
            #     </example>

            #     <chapter>
            #     {chapter.strip()}
            #     </chapter>"""

            # summary 5f
            # prompt = """### INSTRUCTIONS ###
            #     The following types of characters are often found in fictional literature:
            #     - Protagonist
            #     - Antihero
            #     - Antagonist
            #     - Guide
            #     - Contagonist
            #     - Sidekicks (Deuteragonist)
            #     - Henchmen
            #     - Love Interest
            #     - Temptress
            #     - Confidant
            #     - Foil

            #     Given the above list of character types, identify characters in the following chapter from a fictional story that fit these types.
            #     Only use these roles. If no character fits a type, ignore it.
            #     Here is an example: '- Love Interest - Minnie Mouse: Mickey Mouse's lifelong romatic interest.
            #     Format each character like this: 'Character name - Character type: Description'.
            #     ### CHAPTER ###"""

            # summary 5g
            # https://medium.com/@mengsaylms/mastering-prompt-engineering-for-effective-llm-output-tips-techniques-and-warning-d76b09515c3
            # prompt = """### INSTRUCTIONS ###
            #     Provide a bullet-point list of 3 single individual words that best describe the following chapter. Also, provide a brief reason for each word chosen.
            #     Here is an example of a bullet-point: '- Relentless: The riders and thier hounds were desperately chasing after the poor fox.
            #     Don't include the example in the response. Format each bullet-point like this: '- Word: Reason'
            #     ### CHAPTER ###"""

            # summary 5h
            # prompt = """### INSTRUCTIONS ###
            #     The following list of literary devices are often found in fictional literature:
            #     Allegory , Alliteration , Allusion, Amplification , Anagram, Analogy, Anthropomorphism, Antithesis,
            #     Chiasmus, Colloquialism, Circumlocution, Epigraph, Euphemism, Foreshadowing, Hyperbole, Imagery,
            #     Metaphor, Mood, Motif, Onomatopoeia, Oxymoron, Paradox, Personification, Portmanteau, Puns, Satire,
            #     Simile, Symbolism, and Tone.

            #     Based on this list, give 2-3 examples of literary devices found in the following chapter from a fictional story and explain why.
            #     Format each example like this: 'Literary device: Explanation'.
            #     ### CHAPTER ###"""

            # prompt = f"""The following list of literary devices, contained in the <literary_devices> tags below, are often found in fictional literature:
            #     <literary_devices>
            #     Allegory, Alliteration, Allusion, Amplification, Anagram, Analogy, Anthropomorphism, Antithesis,
            #     Chiasmus, Colloquialism, Circumlocution, Epigraph, Euphemism, Foreshadowing, Hyperbole, Imagery,
            #     Metaphor, Mood, Motif, Onomatopoeia, Oxymoron, Paradox, Personification, Portmanteau, Puns, Satire,
            #     Simile, Symbolism, and Tone.
            #     </literary_devices>

            #     Based on this list of literary devices, give 2-3 examples of literary devices found in the chapter in the <chapter> tags below, and explain why.
            #     The Assistant will not use square brackets in its response.

            #     Follow the template contained in the <template> tags below and replace the placeholders with the literary device and the explanation:
            #     <template>
            #     [Literary_Device]: [Explanation]
            #     <template>

            #     <chapter>
            #     {chapter.strip()}
            #     </chapter>"""

            prompt = f"""The following list of character types, contained in the <character_types> tags below, are often found in fictional literature: 
                <character_types>
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
                </character_types>

                Based on this list of character types, give 3-4 examples of character types found in the chapter in the <chapter> tags below, including the character name and an explanation of why.
                The Assistant will not use square brackets in its response.

                Follow the template contained in the <template> tags below and replace the placeholders with the character name, character type, and explanation:
                <template>
                [Character_Name] - [Character_Type]: [Explanation]
                <template>

                Here is an example contained in the <example> tags below:
                <example>
                Love Interest - Minnie Mouse: Mickey Mouse's lifelong romantic interest.
                </example>

                <chapter>
                {chapter.strip()}
                </chapter>"""

            # chapter_summary = utilities.create_summary(client_bedrock, chapter, prompt)
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

    with open(f"../output/{title.lower()}_summary_05l.txt", "w") as f:
        f.write(summary)


if __name__ == "__main__":
    main()
