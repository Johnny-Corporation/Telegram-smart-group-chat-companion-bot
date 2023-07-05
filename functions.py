from os import path, listdir
import json


def load_templates(dir):
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


def load_stickers(file):
    with open(file, "r") as f:
        return json.load(f)


def send_file(path, id, bot):
    with open(path, "rb") as file:
        bot.send_document(id, file)


def send_to_developers(msg, bot, developer_chat_IDs, file=False):
    for id in developer_chat_IDs:
        if id:
            if file:
                send_file(msg, id, bot)
            else:
                bot.send_message(
                    id,
                    msg,
                )


def tokens_to_dollars(model, tokens):
    return "Not implemented"


def convert_to_json(s):
    return (
        s.replace("'", '"')
        .replace("None", "null")
        .replace("True", "true")
        .replace("False", "false")
    )


def send_sticker(chat_id, sticker_id, bot):
    bot.send_sticker(chat_id, sticker_id)
