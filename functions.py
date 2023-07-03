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
