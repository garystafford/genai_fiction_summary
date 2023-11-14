# Mastering Long Document Insights: Advanced Summarization with Amazon Bedrock and Anthropic Claude 2 Foundation Model

Unleash the Power of Generative AI for Comprehensive Document Analysis and Summarization. For more information, see the blog post: [Mastering Long Document Insights: Advanced Summarization with Amazon Bedrock and Anthropic Claude 2 Foundation Model](https://garystafford.medium.com/mastering-long-document-insights-advanced-summarization-with-amazon-bedrock-and-anthropic-claude-2-2fe13d5ae8d8).

## Notebook Examples

The following Jupyter Notebook has all examples included in the blog post and the video: [long_text_summarization_v1.ipynb](long_text_summarization_v1.ipynb). A newer version of the notebook, [long_text_summarization_v2.ipynb](long_text_summarization_v2.ipynb), is also available.


## Commands for Running Scripts

The scripts were written prior to the notebook. The notebook is more current.

```sh
python3 -m pip install virtualenv
virtualenv summarize
python3 -m venv summarize
source summarize/bin/activate

python3 -m pip install -r requirements.txt -Uq

cd older_scripts/
python ./book_summary_05_character.py
```

## Output Examples

```text

2023-10-28 08:29:15,761 - utilities - INFO - Response body: {'completion': ' Here is a single-paragraph description of Count Dracula:\n\nCount Dracula is an ancient vampire of nobility from the remote mountains of Transylvania who resides alone in a decaying yet magnificent castle. He initially appears charming and welcoming but gradually reveals his true sinister and threatening nature. With his gaunt figure, waxen skin, high aquiline nose, pointed ears, sharp teeth and burning red eyes, Dracula exhibits a mysterious magnetism and power over humans, able to control animals and the weather. He attacks the innocent Jonathan Harker, later turning Lucy Westenra into a vampire. Persistent in his vampiric evil, Dracula possesses supernatural abilities and cunning intelligence, escaping capture multiple times. Though eloquent and refined on the surface, at his core Dracula is a ruthless predator who spreads his undead curse, requiring the combined efforts of Dr. Van Helsing and his allies to finally defeat him.', 'stop_reason': 'stop_sequence'}

2023-10-28 14:57:05,196 - utilities - INFO - Response body: {'completion': ' Here are 3 examples of character types from the chapter:\n\nProtagonist - Jonathan Harker: The main protagonist. Struggles against Dracula and tries to protect his wife Mina.\n\nAntagonist - Count Dracula: The main antagonist. A vampire who attacks Mina and opposes the protagonists. \n\nConfidant - Dr. Van Helsing: Acts as a mentor and confidant to the protagonists, guiding them in their fight against Dracula with his knowledge.', 'stop_reason': 'stop_sequence'}

2023-10-28 13:01:27,380 - utilities - INFO - Response body: {'completion': ' Here are 2-3 examples of literary devices found in the chapter:\n\n[Foreshadowing]: The howling of the dogs and wolves foreshadows impending danger and builds suspense. The driver\'s comment "For the dead travel fast" also foreshadows supernatural events to come.\n\n[Imagery]: Vivid imagery is used throughout to describe the scenery, people, and events, such as "the green grass under the trees spangled with the fallen petals". This helps create a rich, immersive setting.\n\n[Personification]: The mountains and cliffs are described as frowning down on the travelers, giving human traits to the landscape. This helps create an ominous, threatening mood.', 'stop_reason': 'stop_sequence'}
```