# from translate import Translator
# import textwrap
# import re
# from utils.functions import *




# supported_languages = {
#     'af': 'afrikaans',
#     'sq': 'albanian',
#     'ar': 'arabic',
#     'hy': 'armenian',
#     'zh': 'chinese',
#     'en': 'english',
#     'fr': 'french',
#     'de': 'german',
#     'ru': 'russian'
# }

# # Ask the user for the target language
# target_language = input("Please enter the language to translate to (e.g., 'ru' or 'russian'): ")

# # The text you want to translate
# templates = load_templates("templates\\")

# txt = templates["account_info.txt"].format(
#         first_name='MichaeLRoman',
#         subscription="SMALL BUSINESS",
#         tokens=3100000,
#         left_tokens = 3094300,
#         groups=3,
#         left_groups=3 - 0,
#         temp_memory_limit=100,
#         temp_memory=20,
#         dyn_gen_per='allowed',
#         voice_in_per='allowed',
#         voice_out_per='allowed',
#         set_up_per='allowed'
#         )#templates["sub_small_business_description.txt"].format(plan="BIG BUSINESS")

# # Check if the entered language is supported
# if target_language not in supported_languages and target_language not in supported_languages.values():
#     print(f"Sorry, the language '{target_language}' is not supported.")
# else:
#     # If the user entered a language name, convert it to the corresponding language code
#     if target_language in supported_languages.values():
#         target_language = list(supported_languages.keys())[list(supported_languages.values()).index(target_language)]

#     # Initialize the Translator object and specify the target language
#     translator = Translator(to_lang="ru")

#     # Define regex patterns
#     command_pattern = r'\/\w+'
#     tag_pattern = r'<\w+>'
#     dollar_pattern = r'\$'
#     emoji_pattern = r'[\U00010000-\U0010ffff]'

#     # Find all patterns in the text
#     commands = re.findall(command_pattern, txt)
#     tags = re.findall(tag_pattern, txt)
#     dollars = re.findall(dollar_pattern, txt)
#     emojis = re.findall(emoji_pattern, txt)

#     # Replace patterns with placeholders
#     for i, command in enumerate(commands):
#         txt = txt.replace(command, f'{{command{i}}}')
#     for i, tag in enumerate(tags):
#         txt = txt.replace(tag, f'{{tag{i}}}')
#     for i, dollar in enumerate(dollars):
#         txt = txt.replace(dollar, f'{{dollar{i}}}')
#     for i, emoji in enumerate(emojis):
#         txt = txt.replace(emoji, f'{{emoji{i}}}')

#     # Split the text into chunks of 4900 characters each
#     chunks = textwrap.wrap(txt, 490)

#     # Translate each chunk and concatenate the translated chunks
#     translated = ""
#     for chunk in chunks:
#         translated_chunk = translator.translate(chunk)
#         translated += translated_chunk

#     # Replace placeholders with original patterns
#     for i, command in enumerate(commands):
#         translated = translated.replace(f'{{command{i}}}', command)
#     for i, tag in enumerate(tags):
#         translated = translated.replace(f'{{tag{i}}}', tag)
#     for i, dollar in enumerate(dollars):
#         translated = translated.replace(f'{{dollar{i}}}', dollar)
#     for i, emoji in enumerate(emojis):
#         translated = translated.replace(f'{{emoji{i}}}', emoji)

#     # The translation is now a string that contains the translated text
#     print(translated)  # "Привет, мир!"










from test import *

def func():
    global templates
    templates = ["YES"]