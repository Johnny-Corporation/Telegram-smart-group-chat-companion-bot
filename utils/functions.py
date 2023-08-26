from os import path, listdir, makedirs, remove, environ, walk
import json
import re
import replicate
from googletrans import Translator
import soundfile as sf
import requests
import zipfile
import xlrd
import openpyxl
import docx2txt
import PyPDF2

from gtts import gTTS
from langdetect import detect

import utils.gpt_interface as gpt


developer_chat_IDs = environ.get("DEVELOPER_CHAT_IDS")
developer_chat_IDs = developer_chat_IDs.split(",")


def read_text_from_xls(file_path):
    workbook = xlrd.open_workbook(file_path)
    sheet = workbook.sheet_by_index(0)

    text_data = []
    for row in range(sheet.nrows):
        for col in range(sheet.ncols):
            cell_value = sheet.cell_value(row, col)
            text_data.append(str(cell_value))

    return "".join(text_data)[:4000]


def read_text_from_xlsx(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    text_data = []
    for row in sheet.iter_rows():
        for cell in row:
            text_data.append(str(cell.value))

    return "".join(text_data)[:4000]


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


def send_image_from_link(bot, url, chat_id):
    "Takes straight url to image and sends it to chat with specified id"
    bot.send_photo(chat_id, url)


def download_and_save_image_from_link(link, filename):
    response = requests.get(link)
    if response.status_code == 200:
        with open("output\\files\\DALLE\\" + filename, "wb") as file:
            file.write(response.content)
            print("Image downloaded successfully.")
    else:
        print("Failed to download image.")


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


def get_file_content(path):
    """Returns file content"""
    try:
        # Download the file
        if path.split(".")[-1] == "xls":
            file_content = read_text_from_xls(path)
        elif path.split(".")[-1] == "xlsx":
            file_content = read_text_from_xlsx(path)
        elif path.split(".")[-1] == "docx":
            file_content = read_word_file(path)

        elif path.split(".")[-1] == "doc":
            file_content = (
                "You cant read content of this file, ask user to send in .docx format"
            )
        elif path.split(".")[-1] == "pdf":
            file_content = extract_text_from_pdf(path)
        else:
            with open(path, "r", encoding="utf-8") as f:
                file_content = f.read()

        return file_content[:2000]
    except Exception as e:
        return "file content cant be read"


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text[:4000]


def read_word_file(file_path):
    text = docx2txt.process(file_path)
    return text[:4000]


def describe_image(link: str, prompt: str = "Describe image") -> str:
    # In our case 50 images approximately 1$
    model = "daanelson/minigpt-4:b96a2f33cc8e4b0aa23eacfce731b9c41a7d9466d9ed4e167375587b54db9423"
    output = replicate.run(
        model,
        input={
            "image": link,
            "prompt": prompt,
        },
    )
    return output


def describe_image2(link: str) -> str:
    model = "salesforce/blip:2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746"
    output = replicate.run(
        model,
        input={"image": link},
    )
    return output.replace("Caption: ", "")


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
    return "".join(random.choice(chars) for _ in range(size))


def check_language(target_language):
    supported_languages = {
        "af": "afrikaans",
        "sq": "albanian",
        "am": "amharic",
        "ar": "arabic",
        "hy": "armenian",
        "az": "azerbaijani",
        "eu": "basque",
        "be": "belarusian",
        "bn": "bengali",
        "bs": "bosnian",
        "bg": "bulgarian",
        "ca": "catalan",
        "ceb": "cebuano",
        "ny": "chichewa",
        "zh-cn": "chinese (simplified)",
        "zh-tw": "chinese (traditional)",
        "co": "corsican",
        "hr": "croatian",
        "cs": "czech",
        "da": "danish",
        "nl": "dutch",
        "en": "english",
        "eo": "esperanto",
        "et": "estonian",
        "tl": "filipino",
        "fi": "finnish",
        "fr": "french",
        "fy": "frisian",
        "gl": "galician",
        "ka": "georgian",
        "de": "german",
        "el": "greek",
        "gu": "gujarati",
        "ht": "haitian creole",
        "ha": "hausa",
        "haw": "hawaiian",
        "iw": "hebrew",
        "he": "hebrew",
        "hi": "hindi",
        "hmn": "hmong",
        "hu": "hungarian",
        "is": "icelandic",
        "ig": "igbo",
        "id": "indonesian",
        "ga": "irish",
        "it": "italian",
        "ja": "japanese",
        "jw": "javanese",
        "kn": "kannada",
        "kk": "kazakh",
        "km": "khmer",
        "rw": "kinyarwanda",
        "ko": "korean",
        "ku": "kurdish (kurmanji)",
        "ky": "kyrgyz",
        "lo": "lao",
        "la": "latin",
        "lv": "latvian",
        "lt": "lithuanian",
        "lb": "luxembourgish",
        "mk": "macedonian",
        "mg": "malagasy",
        "ms": "malay",
        "ml": "malayalam",
        "mt": "maltese",
        "mi": "maori",
        "mr": "marathi",
        "mn": "mongolian",
        "my": "myanmar (burmese)",
        "ne": "nepali",
        "no": "norwegian",
        "or": "odia",
        "ps": "pashto",
        "fa": "persian",
        "pl": "polish",
        "pt": "portuguese",
        "pa": "punjabi",
        "ro": "romanian",
        "ru": "russian",
        "sm": "samoan",
        "gd": "scots gaelic",
        "sr": "serbian",
        "st": "sesotho",
        "sn": "shona",
        "sd": "sindhi",
        "si": "sinhala",
        "sk": "slovak",
        "sl": "slovenian",
        "so": "somali",
        "es": "spanish",
        "su": "sundanese",
        "sw": "swahili",
        "sv": "swedish",
        "tg": "tajik",
        "ta": "tamil",
        "tt": "tatar",
        "te": "telugu",
        "th": "thai",
        "tr": "turkish",
        "tk": "turkmen",
        "uk": "ukrainian",
        "ur": "urdu",
        "ug": "uyghur",
        "uz": "uzbek",
        "vi": "vietnamese",
        "cy": "welsh",
        "xh": "xhosa",
        "yi": "yiddish",
        "yo": "yoruba",
        "zu": "zulu",
    }

    # Check if the entered language is supported
    if (
        target_language not in supported_languages
        and target_language not in supported_languages.values()
    ):
        return False
    else:
        # If the user entered a language name, convert it to the corresponding language code
        if target_language in supported_languages.values():
            target_language = list(supported_languages.keys())[
                list(supported_languages.values()).index(target_language)
            ]

            return [target_language, supported_languages[target_language]]
        elif target_language in supported_languages.keys():
            return [target_language, supported_languages[target_language]]


def translate_templates(lang):
    # Regular expression to match /command commands and HTML tags
    command_regex = re.compile(r"(  /.*? |<.*?>|{.*?})")

    # Initialize the Translator object and specify the target language
    translator = Translator()

    # Directory where the translated files will be saved
    target_directory = f"templates/{lang}"

    # Check if the target directory already exists
    if path.exists(target_directory):
        print(
            f"The directory '{target_directory}' already exists. Skipping translation."
        )
    else:
        # Create the target directory
        makedirs(target_directory)

        # Directory containing the source text files
        source_directory = "templates/en"

        # Translate each text file in the source directory
        for filename in listdir(source_directory):
            # Only process .txt files
            if filename.endswith(".txt"):
                # Read the source file
                with open(path.join(source_directory, filename), "r") as file:
                    txt = file.read()

                # Find all matches of the regular expression in the text
                matches = command_regex.findall(txt)

                # Replace the matches with placeholders
                for i, match in enumerate(matches):
                    placeholder = f"{{{i}}}"
                    txt = txt.replace(match, placeholder, 1)

                # Split the text into chunks of 500 characters each
                chunks = [txt[i : i + 500] for i in range(0, len(txt), 500)]

                # Translate each chunk and join them together
                translation = "".join(
                    [translator.translate(chunk, dest=lang).text for chunk in chunks]
                )

                # Replace the placeholders with the original text
                for i, match in enumerate(matches):
                    placeholder = f"{{{i}}}"
                    translation = translation.replace(placeholder, match, 1)

                # Write the translated text to a new file in the target directory
                with open(
                    path.join(target_directory, filename), "w", encoding="utf-8"
                ) as file:
                    file.write(translation)


def translate_text(lang, text):
    if lang == "en":
        return text
    else:
        translator = Translator()
        translated = translator.translate(text, dest=lang)
        return translated.text


def load_buttons(types, groups, chat_id, language_code, owner_id=None):
    print("IAM IN LOADBUTTONS")
    print(f"ENABLING: {groups[chat_id].enabled}")
    print(f"CHAT_ID: {chat_id}")

    groups[chat_id].button_commands = []

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    if chat_id > 0:
        if groups[chat_id].enabled == True:
            text2 = translate_text(language_code, "ㅤStart a conversation from scratchㅤ")
            itembtn1 = types.KeyboardButton(text2)

        elif groups[chat_id].enabled == False:
            text2 = translate_text(language_code, "ㅤStart a conversationㅤ")
            itembtn1 = types.KeyboardButton(text2)

        if str(chat_id) in developer_chat_IDs:
            text_dev_tools = translate_text(language_code, "/dev_tools")
            itembtn_dev_tools = types.KeyboardButton(text_dev_tools)
            markup.add(itembtn_dev_tools)

        text1 = translate_text(language_code, "ㅤAsk a question without contextㅤ")
        itembtn2 = types.KeyboardButton(text1)

        text5 = translate_text(language_code, "ㅤAccountㅤ")
        itembtn4 = types.KeyboardButton(text5)

        text6 = translate_text(language_code, "ㅤSettingsㅤ")
        itembtn5 = types.KeyboardButton(text6)

        text8 = translate_text(language_code, "ㅤReport bugㅤ")
        itembtn6 = types.KeyboardButton(text8)

        text9 = translate_text(language_code, "ㅤSuggest an ideaㅤ")
        itembtn7 = types.KeyboardButton(text9)

        groups[chat_id].button_commands.append(text2)
        groups[chat_id].button_commands.append(text1)

        markup.add(itembtn1)
        markup.add(itembtn2)
        markup.add(itembtn4)
        markup.add(itembtn5)
        markup.add(itembtn6, itembtn7)

        groups[chat_id].button_commands.append(text5)
        groups[chat_id].button_commands.append(text6)
        groups[chat_id].button_commands.append(text8)
        groups[chat_id].button_commands.append(text9)

    elif chat_id < 0:
        print("GROUP CONDITION")

        if owner_id == None:
            text1 = translate_text(language_code, "ㅤActivate botㅤ")
            itembtn1 = types.KeyboardButton(text1)
            text2 = translate_text(language_code, "ㅤAboutㅤ")
            itembtn2 = types.KeyboardButton(text2)
            markup.add(itembtn1)
            markup.add(itembtn2)

            groups[chat_id].button_commands.append(text1)
            groups[chat_id].button_commands.append(text2)

            return markup

        print(groups[chat_id].enabled)
        if groups[chat_id].enabled == True:
            print("ENABLED")
            text1 = translate_text(language_code, "ㅤStop conversationㅤ")
            itembtn1 = types.KeyboardButton(text1)

        elif groups[chat_id].enabled == False:
            text1 = translate_text(language_code, "ㅤStart a conversationㅤ")
            itembtn1 = types.KeyboardButton(text1)

        text2 = translate_text(language_code, "ㅤAsk a question without contextㅤ")
        itembtn2 = types.KeyboardButton(text2)

        text5 = translate_text(language_code, "ㅤGroupㅤ")
        itembtn5 = types.KeyboardButton(text5)

        text6 = translate_text(language_code, "ㅤSettingsㅤ")
        itembtn6 = types.KeyboardButton(text6)

        text7 = translate_text(language_code, "ㅤReport bugㅤ")
        itembtn7 = types.KeyboardButton(text7)

        text8 = translate_text(language_code, "ㅤSuggest an ideaㅤ")
        itembtn8 = types.KeyboardButton(text8)

        # text10 = translate_text(language_code,'ㅤSupport usㅤ')
        # itembtn10 = types.KeyboardButton(text10)
        # groups[chat_id].button_commands.append(text10)

        groups[chat_id].button_commands.append(text1)
        groups[chat_id].button_commands.append(text2)

        markup.add(itembtn1)
        markup.add(itembtn2)

        if groups[chat_id].enabled == True:
            text3 = translate_text(language_code, "ㅤView current modeㅤ")
            itembtn3 = types.KeyboardButton(text3)
            groups[chat_id].button_commands.append(text3)
            markup.add(itembtn3)
            text4 = translate_text(language_code, "ㅤChange modeㅤ")
            itembtn4 = types.KeyboardButton(text4)
            groups[chat_id].button_commands.append(text4)
            markup.add(itembtn4)

        markup.add(itembtn5)
        markup.add(itembtn6)
        markup.add(itembtn7, itembtn8)
        # markup.add(itembtn10)

        groups[chat_id].button_commands.append(text5)
        groups[chat_id].button_commands.append(text6)
        groups[chat_id].button_commands.append(text7)
        groups[chat_id].button_commands.append(text8)

        print(f"TEXTS OF BUTTONS : {groups[chat_id].button_commands}")

        return markup

    return markup


def to_text(bot, message, reply_to=None):
    """Take a voice message + circle and translate to text"""

    if reply_to != None:
        message = reply_to

    file_name_full = "output\\voice_in\\" + message.voice.file_id + ".ogg"
    file_name_full_converted = "output\\voice_in\\" + message.voice.file_id + ".wav"
    file_info = bot.get_file(message.voice.file_id)

    makedirs("output\\voice_in", exist_ok=True)

    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, "wb") as new_file:
        new_file.write(downloaded_file)

    # Load ogg file
    data, samplerate = sf.read(file_name_full)

    # Export as wav
    sf.write(file_name_full_converted, data, samplerate)

    # Delete .ogg file
    remove(file_name_full)

    text = gpt.speech_to_text(file_name_full_converted)

    remove(file_name_full_converted)

    return text


def generate_voice_message(message, text, language, reply_to=None):
    """Got a text and generate voice file and return path to voice file"""

    if reply_to != None:
        message = reply_to

    voice_obj = gTTS(text=text, lang=language, slow=False)

    if not path.exists("output\\voice_out"):
        makedirs("output\\voice_out")

    voice_obj.save(f"output\\voice_out\\voice_out_{message.message_id}.mp3")

    return f"output\\voice_out\\voice_out_{message.message_id}.mp3"


def video_note_to_audio(bot, message, reply_to=None):
    print("!!!!!!!!!!!!!!!!!!!!!!!!")

    video_file_path = f"output\\video_notes\\video_note_{message.message_id}.mp4"
    audio_file_path = f"output\\video_notes\\audio_{message.message_id}.mp3"

    file_info = bot.get_file(message.video_note.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(video_file_path, "wb") as new_file:
        new_file.write(downloaded_file)

    video = VideoFileClip(video_file_path)
    video.audio.write_audiofile(audio_file_path)

    text = gpt.speech_to_text(audio_file_path)

    return text


def take_info_about_sub(subscription):
    subscriptions = {
        "Free": {  # {type_of_sub: {point: value_of_point}}
            "allowed_groups": 1,
            "messages_limit": 30,
            "temporary_memory_size_limit": 20,
            "dynamic_gen_permission": False,
            "sphere_permission": False,
            "temperature_permission": False,
            "frequency_penalty_permission": False,
            "presense_penalty_permission": False,
            "voice_output_permission": False,
            "generate_picture_permission": False,
        },
        "USER": {
            "allowed_groups": 3,
            "messages_limit": 100,
            "temporary_memory_size_limit": 50,
            "dynamic_gen_permission": False,
            "sphere_permission": False,
            "temperature_permission": False,
            "frequency_penalty_permission": False,
            "presense_penalty_permission": False,
            "voice_output_permission": False,
            "generate_picture_permission": False,
        },
        "SMALL BUSINESS": {
            "allowed_groups": 5,
            "messages_limit": 300,
            "temporary_memory_size_limit": 100,
            "dynamic_gen_permission": True,
            "sphere_permission": True,
            "temperature_permission": True,
            "frequency_penalty_permission": True,
            "presense_penalty_permission": True,
            "voice_output_permission": True,
            "generate_picture_permission": True,
        },
        "SMALL BUSINESS (trial)": {
            "allowed_groups": 5,
            "messages_limit": 50,
            "temporary_memory_size_limit": 100,
            "dynamic_gen_permission": True,
            "sphere_permission": True,
            "temperature_permission": True,
            "frequency_penalty_permission": True,
            "presense_penalty_permission": True,
            "voice_output_permission": True,
            "generate_picture_permission": True,
        },
        "BIG BUSINESS": {
            "allowed_groups": 10,
            "messages_limit": 500,
            "temporary_memory_size_limit": 1000000000000000000,
            "dynamic_gen_permission": True,
            "sphere_permission": True,
            "temperature_permission": True,
            "frequency_penalty_permission": True,
            "presense_penalty_permission": True,
            "voice_output_permission": True,
            "generate_picture_permission": True,
        },
    }

    permissions = subscriptions[subscription]

    return permissions


def read_text_from_image(url):
    headers = {"apikey": environ["API_LAYER_TOKEN"]}

    response = requests.get(
        "https://api.apilayer.com/image_to_text/url?url=" + url, headers=headers
    )

    status_code = response.status_code
    result = response.text

    print(status_code)
    print(result)

    if "all_text" in response.json():
        return response.json()["all_text"][:2000]
    else:
        return "No text detected!"


def get_avaible_langs():
    folder_path = ".\\templates"

    return [d for d in listdir(folder_path) if path.isdir(path.join(folder_path, d))]

    # folder_path = '/path/to/your/folder'
    # directories = list_directories(folder_path)
    # print(directories)


def create_archive(folder_path, output_path):
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for folder_root, _, files in walk(folder_path):
            for file in files:
                file_path = path.join(folder_root, file)
                archive_path = path.relpath(file_path, folder_path)
                archive.write(file_path, archive_path)
