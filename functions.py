from os import path, listdir
import json


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
