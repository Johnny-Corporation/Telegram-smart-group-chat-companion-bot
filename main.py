# Bot API
from telebot import TeleBot

# Local modules
from Johnny import Johnny
from internet_access import *
from functions import *
import gpt_functions as gpt

# Other
from dotenv import load_dotenv
from os import environ, path, mkdir
import logging
import traceback
from datetime import datetime




load_dotenv(".env")

# Needed for filtering messages when bot was offline
start_time = datetime.now()
skip_old_messages = True
ignored_messages = 0  # count number of ignored messages when bot was offline for logs



logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)





#------------------------------------------------------------------Loading the tokens/templates/token---------------------------------------------------------------------------------------------------

# --- loading tokens ---
bot_token = environ.get("BOT_API_TOKEN")
developer_chat_IDs = environ.get("DEVELOPER_CHAT_IDS")
gpt_token = environ.get("OPENAI_API_KEY")
organization_token = environ.get("OPENAI_ORGANIZATION")

if not bot_token:
    logger.error("Failed to load BOT_API_TOKEN from environment, exiting...")
    exit()
if not developer_chat_IDs:
    logger.warning("Developers chat ids is not set!")
else:
    developer_chat_IDs = developer_chat_IDs.split(",")
if not gpt_token:
    logger.error("Failed to load OPEN_API_TOKEN from environment, exiting...")
if not organization_token:
    logger.error("Failed to load OPENAI_ORGANIZATION from environment, exiting...")


# --- loading templates/stickers ---
templates = load_templates("templates\\")
stickers = load_stickers("stickers.json")
language_code = "en"


# --- blacklist ---
blacklist = {}  # chat_id:[messages_ids] needed for filtering messages
reply_blacklist = {}  # chat_id:[messages_ids] needed for filtering replies to messages


#??????????????????????????????
if not path.exists("groups_info"):
    mkdir("groups_info")


# --- Initialazing a bot ----
bot = TeleBot(bot_token)
bot_id = bot.get_me().id
bot_username = bot.get_me().username


groups = {}  # {id:Johnny object}


# --- error handler ---
def error_handler(func):
    def wrapper(message):
        try:
            func(message)
        except Exception as e:
            logger.error(f"Unexpected error: {traceback.format_exc()}")
            bot.send_message(
                message.chat.id,
                "Sorry, unexpected error occurred, developer has been already notified!",
            )
            send_to_developers(
                f"Error occurred!!!: \n -----------\n {traceback.format_exc()}\n ---------- ",
                bot,
                developer_chat_IDs,
            )
            send_to_developers("logs.log", bot, developer_chat_IDs, file=True)
        else:
            logger.info(
                f"Command {message.text} executed in chat with id {message.chat.id}"
            )
            # log gpt responses

    return wrapper


# --- filter messages which sent not in working bot ---
def time_filter(message):
    """Filters message which were sent before bot start"""
    global skip_old_messages, ignored_messages
    if not skip_old_messages:
        return True
    message_time = datetime.fromtimestamp(message.date)
    if start_time < message_time:
        skip_old_messages = False
        logger.warning(
            f"{ignored_messages} messages have been ignored since last start."
        )
        return True
    else:
        ignored_messages += 1
        return False





#---------------------------------------------------------------------Bot_messages-----------------------------------------------------------------------------------------------------------------


# --- Help ---
@bot.message_handler(commands=["help"], func=time_filter)
@error_handler
def error_command(message):
    bot.reply_to(message, templates[language_code]["help.txt"], parse_mode="Markdown")


# --- Tokens info ---
@bot.message_handler(commands=["tokens_info"], func=time_filter)
@error_handler
def tokens_info_command(message):
    bot.reply_to(
        message,
        templates[language_code]["tokens.txt"].format(dollars=0, spent_tokens=0),
    )


# --- About ---
@bot.message_handler(commands=["about", "start"], func=time_filter)
@error_handler
def about_command(message):
    bot.reply_to(message, templates[language_code]["description.txt"])


# --- reply handler for feature requests ---
@error_handler
def feature_request_reply_handler(inner_message):
    user = inner_message.from_user
    send_to_developers(
        f"""User {user.first_name} {user.last_name} (@{user.username}) 
            from group with name {inner_message.chat.title} requested a feature! 
            Here is what he said: 
            {inner_message.text}""",
        bot,
        developer_chat_IDs,
    )
    bot.reply_to(
        inner_message,
        templates[language_code]["feature_request_thanks.txt"],
    )


# --- reply handler for bug reports ---
@error_handler
def bug_report_reply_handler(inner_message):
    user = inner_message.from_user
    send_to_developers(
        f"""User {user.first_name} {user.last_name} (@{user.username}) 
            from group with name {inner_message.chat.title} reported a bug! 
            Here is what he said: 
            {inner_message.text}""",
        bot,
        developer_chat_IDs,
    )
    bot.reply_to(
        inner_message,
        templates[language_code]["bug_report_thanks.txt"],
    )


# --- Report bug ---
@bot.message_handler(commands=["report_bug"], func=time_filter)
@error_handler
def report_bug_command(message):
    bot_reply = bot.reply_to(message, templates[language_code]["report_bug.txt"])
    if message.chat.id not in reply_blacklist:
        reply_blacklist[message.chat.id] = [bot_reply.message_id]
    else:
        reply_blacklist.append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, bug_report_reply_handler)


# --- Request feature ---
@bot.message_handler(commands=["request_feature"], func=time_filter)
@error_handler
def request_feature_command(message):
    bot_reply = bot.reply_to(message, templates[language_code]["request_feature.txt"])
    if message.chat.id not in reply_blacklist:
        reply_blacklist[message.chat.id] = [bot_reply.message_id]
    else:
        reply_blacklist.append(bot_reply.message_id)
    bot.register_for_reply(bot_reply, feature_request_reply_handler)


# --- Set temp ---
@bot.message_handler(commands=["set_temperature"], func=time_filter)
@error_handler
def set_temp_command(message):
    # logic (check val from 0 to 1!)
    bot.reply_to(message, "Not implemented")


# --- Handling new groups ---
@bot.message_handler(content_types=["new_chat_members"], func=time_filter)
@error_handler
def handle_new_chat_members(message):
    for new_chat_member in message.new_chat_members:
        if new_chat_member.id == bot_id:
            init_new_group(message.chat.id)





def init_new_group(chat_id):
    bot.send_message(chat_id, templates["new_group_welcome.txt"])
    send_sticker(chat_id, stickers["initializing"], bot)
    bot.send_message(
        chat_id,
        "Initializing...",
    )
    with open(
        f"groups_info\\{bot.get_chat(chat_id).title}.json",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(convert_to_json(str(bot.get_chat(chat_id))))
    blacklist[chat_id] = []
    reply_blacklist[chat_id] = []

    johnny = Johnny(bot, chat_id, logger, bot_username)
    if not Johnny:
        logger.error("The object didn't initialized")
    else:    
        logger.info("The class was initialized")
    groups[chat_id] = johnny
    return johnny


# --- blacklist filters ---
def blacklist_filter(message):
    if message.chat.id not in blacklist:
        return True
    return not (message.message_id in blacklist.get(message.chat.id))


def reply_blacklist_filter(message):
    if message.chat.id not in reply_blacklist:
        return True
    return (message.reply_to_message is None) or (
        message.reply_to_message.message_id not in reply_blacklist[message.chat.id]
    )



# ------------------------- Gameplay functions ----------------------------

# --- Enable automatic setting up --- (work through Johnny)
@bot.message_handler(commands=["enable"], func=time_filter)
@error_handler
def enable_command(message):
    groups[message.chat.id].enabled = True
    if language_code == "en":
        return bot.reply_to(message, templates[language_code]["enabled.txt"])
    bot.send_sticker(message.chat.id, stickers["enable"])
    

# --- Disable automatic setting up ---
@bot.message_handler(commands=["disable"], func=time_filter)
@error_handler
def disable_command(message):
    groups[message.chat.id].enabled = False
    bot.reply_to(message, templates[language_code]["disabled.txt"])


# --- ask one question to bot ---
@bot.message_handler(commands=['question'])
@error_handler
def question_to_bot(message):
    bot.send_message(message.chat.id, gpt.question_to_bot(gpt_token,organization_token,message.text),parse_mode='HTML')


model = "gpt-3.5-turbo"
temporary_memory = []

# --- turn on dialog mode ---
@bot.message_handler(commands=["start_dialog"])
def start_dialog(message):

    full_message = message.text
    message_to_gpt = ''
    system_content = 'Have a dialogue, be a friendly helper'    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Can be changed!!!!!!!!!!!!!
    
    bot.send_message(message.chat.id, "Dialog was started.\nIf you want to end it write\n/end_conservation",parse_mode='HTML')     #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Can be changed!!!!!!!!!!!!!!

    #Split the command /start and 'message after this' - message_to_gpt
    temporary_memory.append('/start')
    try:
        for i in range(full_message.index(' ')+1, len(full_message)):
            message_to_gpt = message_to_gpt + full_message[i]

        response = gpt.get_response(gpt.message_to_ai(gpt_token,organization_token,model,system_content,message_to_gpt))

        temporary_memory.append([message_to_gpt,response])

        bot.send_message(message.chat.id, response,parse_mode='HTML')

    except:
        print('')
 
# --- turn off dialog mode ---
@bot.message_handler(commands=["end_dialog"])
def end_dialog(message):
    bot.send_message(message.chat.id, "The conservation ended",parse_mode='HTML')     #!!!!!!!!!!!!!!!!!!!!!!!!!!!!Can be changed!!!!!!!!!!!!!!!!
    temporary_memory.clear()


















@bot.message_handler(
    func=lambda message: reply_blacklist_filter(message)
    and blacklist_filter(message)
    and time_filter(message)
)
def main_messages_handler(message):
    
    # --- check the registration of group and interaction with usual nessages ---
    if message.chat.id not in groups:
        bot.send_message(message.chat.id, templates[language_code]["after_restart.txt"])
        johnny = init_new_group(message.chat.id)
        johnny.load_data()

        #     # --- command filter ---
        # if message.text[0] == '/':
        #     return 'Incorrect command.\n/help for list of messages'

    else:
        if response := groups[message.chat.id].new_message(message):
            bot.send_message(message.chat.id, response)




    #     if'/start' in temporary_memory:
    #         bot.send_message(message.chat.id, 'Your dialog is still going', parse_mode='HTML')
    









    











logger.info("Bot started")
bot.polling()
