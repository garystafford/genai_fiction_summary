# Summarize a Large Text File

```sh
python3 -m pip install virtualenv
virtualenv summarize
python3 -m venv summarize
source summarize/bin/activate

python3 -m pip install -r requirements.txt -Uq

black *.py
```


```text
2023-10-23 20:22:15,461 - utilities - INFO - Response body: {'completion': ' Here are two examples of literary devices from the passage:\n\nForeshadowing: Van Helsing rubs garlic flowers over Lucy\'s window and door, saying "Perhaps I am!" working some spell to keep out an evil spirit. This foreshadows supernatural events involving Lucy later in the story.\n\nImagery: Descriptions of Lucy like "horribly white and wan-looking" and "the pallid cheeks and lips" create vivid imagery related to her illness and loss of blood.\n\nThe foreshadowing builds suspense and hints at future plot developments, while the imagery helps the reader visualize Lucy\'s worsening condition. The literary devices add to the gothic tone and drama of this scene.', 'stop_reason': 'stop_sequence'}

2023-10-23 20:22:44,134 - utilities - INFO - Response body: {'completion': ' Here are some examples of literary devices from the chapter:\n\nForeshadowing: "Somehow, I do not dread being alone to-night, and I can go to sleep without fear." This foreshadows the later events of Lucy being attacked by the wolf.\n\nImagery: "The air seems full of specks, floating and circling in the draught from the window, and the lights burn blue and dim." This imagery creates a vivid scene for the reader.\n\nSymbolism: The flowers around Lucy\'s neck represent her innocence and purity. When the wolf tears them off, it symbolizes the loss of that innocence. \n\nPersonification: "Presently the door opened, and mother looked in; seeing by my moving that I was not asleep, came in, and sat by me." The door is personified as opening on its own.\n\nSimile: "I tried to stir, but there was some spell upon me, and dear mother’s poor body, which seemed to grow cold already—for her dear heart had ceased to beat—weighed me down; and I remembered no more for a while." This compares the feeling of being weighed down to her mother\'s body on top of her.', 'stop_reason': 'stop_sequence'}```