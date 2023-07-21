from os import path, listdir, makedirs
import json
import re
from googletrans import Translator
from bs4 import BeautifulSoup, NavigableString
import textwrap
#import tiktoken


def load_templates(dir: str) -> dict:
    """Get templates dict {language_code: {file_name: content}}

    Args:
        dir (str): path to directory with templates

    Returns:
        dict
    """
    file_dict = {}
    for language_code in listdir(dir):
        if path.isfile(path.join(dir, language_code)):
            with open(path.join(dir, language_code), "r") as f:
                file_dict[language_code] = f.read()
            continue
        for file_name in listdir(path.join(dir, language_code)):
            if file_name.endswith(".txt"):
                file_path = path.join(dir, language_code, file_name)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    if language_code not in file_dict:
                        file_dict[language_code] = {file_name: content}
                    else:
                        file_dict[language_code][file_name] = content
    return file_dict


def load_stickers(file: str) -> dict:
    """Returns stickers dict {sticker_name: sticker_id}

    Args:
        file (str): path to file with stickers

    Returns:
        dictionary
    """
    with open(file, "r") as f:
        return json.load(f)


def send_file(path: str, id: int, bot) -> None:
    """Sends a file to chat

    Args:
        path (str): path to file
        id (int): chat id
        bot (_type_): TeleBot object
    """
    with open(path, "rb") as file:
        bot.send_document(id, file)


def send_to_developers(
    msg: str, bot, developer_chat_IDs: list, file: bool = False
) -> None:
    """Sends message or file to developers (all chats with specified ids)

    Args:
        msg (str): message text or file name if file is set to True
        bot (_type_): Telebot object
        developer_chat_IDs (list): list of integers - chat ids
        file (bool, optional): If set to true, msg is considered as file name. Defaults to False.
    """
    for id in developer_chat_IDs:
        if id:
            if file:
                send_file(msg, id, bot)
            else:
                bot.send_message(
                    id,
                    msg,
                )


def tokens_to_dollars(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Converts tokens to dollars

    Args:
        model (str): model name (ex: gpt-3.5-turbo)
        input_tokens (int)
        output_tokens (int)

    Returns:
        float
    """
    coefficients = {
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
        "gpt-3.5-turbo-16k": {"input": 0.003, "output": 0.004},
    }
    input_price = (prompt_tokens / 1000) * coefficients[model]["input"]
    output_price = (completion_tokens / 1000) * coefficients[model]["output"]
    return input_price + output_price


def convert_to_json(s: str) -> str:
    """Converts python dict in string format to json

    Args:
        s (str)

    Returns:
        str
    """
    return (
        s.replace("'", '"')
        .replace("None", "null")
        .replace("True", "true")
        .replace("False", "false")
    )


def send_sticker(chat_id: int, sticker_id: str, bot) -> None:
    """Sends sticker to chat

    Args:
        chat_id (int)
        sticker_id (str)
        bot (_type_): Telebot object
    """
    bot.send_sticker(chat_id, sticker_id)


def tokenize(text: str) -> int:
    """Takes text and returns number of tokens

    Args:
        text (str)
    Returns:
        tokens (int)
    """
    raise NotImplementedError("Make this please")


def remove_utf8_chars(string: str) -> str:
    """Removes all strange chars, if all symbols were removed, returns "empty" """
    # Use a regular expression to remove non-alphanumeric characters
    cleaned_string = re.sub(r"[^a-zA-Z0-9]", "", string).replace(".", "")

    if not cleaned_string:
        cleaned_string = "empty"
    return cleaned_string


def clean_string(string: str) -> str:
    """Removes all strange chars, if all symbols were removed, returns "empty" """
    # Use a regular expression to remove non-alphanumeric characters and non-Russian letters
    cleaned_string = re.sub(r"[^a-zA-Z0-9а-яА-ЯёЁ]", "", string).replace(".", "")

    if not cleaned_string:
        cleaned_string = "empty"
    return cleaned_string


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print(
            "Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613."
        )
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print(
            "Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613."
        )
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def check_file_existing(client_first_name, file_path):
    clients = listdir(file_path)
                    
    for filename in clients:
        if client_first_name in filename:
             return True
        else:
            return False
                                
    if clients == []:
        return False
    

def generate_code():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(size))


def check_language(target_language):
    supported_languages = {
        'af': 'afrikaans',
        'sq': 'albanian',
        'am': 'amharic',
        'ar': 'arabic',
        'hy': 'armenian',
        'az': 'azerbaijani',
        'eu': 'basque',
        'be': 'belarusian',
        'bn': 'bengali',
        'bs': 'bosnian',
        'bg': 'bulgarian',
        'ca': 'catalan',
        'ceb': 'cebuano',
        'ny': 'chichewa',
        'zh-cn': 'chinese (simplified)',
        'zh-tw': 'chinese (traditional)',
        'co': 'corsican',
        'hr': 'croatian',
        'cs': 'czech',
        'da': 'danish',
        'nl': 'dutch',
        'en': 'english',
        'eo': 'esperanto',
        'et': 'estonian',
        'tl': 'filipino',
        'fi': 'finnish',
        'fr': 'french',
        'fy': 'frisian',
        'gl': 'galician',
        'ka': 'georgian',
        'de': 'german',
        'el': 'greek',
        'gu': 'gujarati',
        'ht': 'haitian creole',
        'ha': 'hausa',
        'haw': 'hawaiian',
        'iw': 'hebrew',
        'he': 'hebrew',
        'hi': 'hindi',
        'hmn': 'hmong',
        'hu': 'hungarian',
        'is': 'icelandic',
        'ig': 'igbo',
        'id': 'indonesian',
        'ga': 'irish',
        'it': 'italian',
        'ja': 'japanese',
        'jw': 'javanese',
        'kn': 'kannada',
        'kk': 'kazakh',
        'km': 'khmer',
        'rw': 'kinyarwanda',
        'ko': 'korean',
        'ku': 'kurdish (kurmanji)',
        'ky': 'kyrgyz',
        'lo': 'lao',
        'la': 'latin',
        'lv': 'latvian',
        'lt': 'lithuanian',
        'lb': 'luxembourgish',
        'mk': 'macedonian',
        'mg': 'malagasy',
        'ms': 'malay',
        'ml': 'malayalam',
        'mt': 'maltese',
        'mi': 'maori',
        'mr': 'marathi',
        'mn': 'mongolian',
        'my': 'myanmar (burmese)',
        'ne': 'nepali',
        'no': 'norwegian',
        'or': 'odia',
        'ps': 'pashto',
        'fa': 'persian',
        'pl': 'polish',
        'pt': 'portuguese',
        'pa': 'punjabi',
        'ro': 'romanian',
        'ru': 'russian',
        'sm': 'samoan',
        'gd': 'scots gaelic',
        'sr': 'serbian',
        'st': 'sesotho',
        'sn': 'shona',
        'sd': 'sindhi',
        'si': 'sinhala',
        'sk': 'slovak',
        'sl': 'slovenian',
        'so': 'somali',
        'es': 'spanish',
        'su': 'sundanese',
        'sw': 'swahili',
        'sv': 'swedish',
        'tg': 'tajik',
        'ta': 'tamil',
        'tt': 'tatar',
        'te': 'telugu',
        'th': 'thai',
        'tr': 'turkish',
        'tk': 'turkmen',
        'uk': 'ukrainian',
        'ur': 'urdu',
        'ug': 'uyghur',
        'uz': 'uzbek',
        'vi': 'vietnamese',
        'cy': 'welsh',
        'xh': 'xhosa',
        'yi': 'yiddish',
        'yo': 'yoruba',
        'zu': 'zulu'
    }

    # Check if the entered language is supported
    if target_language not in supported_languages and target_language not in supported_languages.values():
        return False
    else:
        # If the user entered a language name, convert it to the corresponding language code
        if target_language in supported_languages.values():
            target_language = list(supported_languages.keys())[list(supported_languages.values()).index(target_language)]

            return [target_language, supported_languages[target_language]]
        elif target_language in supported_languages.keys():
            return [target_language, supported_languages[target_language]]

def translate_templates(lang):

    # Regular expression to match /command commands and HTML tags
    command_regex = re.compile(r'(  /.*? |<.*?>|{.*?})')

    # Initialize the Translator object and specify the target language
    translator = Translator()

    # Directory where the translated files will be saved
    target_directory = f'templates/{lang}'

     # Check if the target directory already exists
    if path.exists(target_directory):
        print(f"The directory '{target_directory}' already exists. Skipping translation.")
    else:
        # Create the target directory
        makedirs(target_directory)

        # Directory containing the source text files
        source_directory = 'templates/en'

        # Translate each text file in the source directory
        for filename in listdir(source_directory):
            # Only process .txt files
            if filename.endswith('.txt'):
                # Read the source file
                with open(path.join(source_directory, filename), 'r') as file:
                    txt = file.read()

                # Find all matches of the regular expression in the text
                matches = command_regex.findall(txt)

                # Replace the matches with placeholders
                for i, match in enumerate(matches):
                    placeholder = f'{{{i}}}'
                    txt = txt.replace(match, placeholder, 1)

                # Split the text into chunks of 500 characters each
                chunks = [txt[i:i + 500] for i in range(0, len(txt), 500)]

                # Translate each chunk and join them together
                translation = ''.join([translator.translate(chunk, dest=lang).text for chunk in chunks])

                # Replace the placeholders with the original text
                for i, match in enumerate(matches):
                    placeholder = f'{{{i}}}'
                    translation = translation.replace(placeholder, match, 1)

                # Write the translated text to a new file in the target directory
                with open(path.join(target_directory, filename), 'w', encoding="utf-8") as file:
                    file.write(translation)


def translate_text(lang, text):
    if lang == 'en':
        return text
    else:
        translator = Translator()
        translated = translator.translate(text, dest=lang)
        return translated.text