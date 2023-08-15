from os import path, listdir
import json
import re
import replicate


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


def get_file_content(bot, message):
    """Returns file content"""
    try:
        # Download the file
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Convert the file's binary content to string
        file_content = downloaded_file.decode("utf-8")

        # Send back the first 1000 characters of the file (to avoid message length limits)
        return file_content[:1000]
    except Exception as e:
        return "file content cant be read"


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
