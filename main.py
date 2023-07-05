# GPT API
import openai

# Bot API
from telebot import TeleBot

# Local modules
from templates_loader import load_templates
from Johnny import Johnny
from internet_access import *
import GPT_FUNCS as gpt

# Other
from dotenv import load_dotenv, find_dotenv
from os import environ, getenv
import logging
import traceback
import json  # groups.json write groups in file !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

load_dotenv('.env')

#---------------------------------laying-----------------------------


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

#---------------------------------Loading the tokens/templates/token---------------------------------------------------------------------------------------------------


bot_token = environ.get("BOT_API_TOKEN")
openAI_api_key = environ.get("OPENAI_API_KEY1")
openAI_organization_key = environ.get("OPENAI_ORGANIZATION")
developer_chat_IDs = environ.get("DEVELOPER_CHAT_IDS")

if not all((bot_token, openAI_api_key)):                    #Got it or not
    logger.error(
        "Failed to load OPENAI_API_KEY or BOT_API_TOKEN from environment, exiting..."
    )
    exit()
if not developer_chat_IDs:
    logger.warning("Developers chat ids is not set!")
else:
    developer_chat_IDs = developer_chat_IDs.split(",")



templates = load_templates("templates\\")

#initial api_key
openai.api_key = openAI_api_key


def tokens_to_dollars(model, tokens):
    return "Not implemented"


bot = TeleBot(bot_token)
bot_id = bot.get_me().id


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
                f"Error occurred!!!: \n -----------\n {traceback.format_exc()}\n ---------- "
            )
            send_to_developers("logs.log", file=True)
        else:
            logger.info(
                f"Command {message.text} executed in chat with id {message.chat.id}"
            )
            # log gpt responses

    return wrapper



#---------------------------------------------------------------Functions------------------------------------------------------------------------------------------------------------

def send_file(path, id):
    with open(path, "rb") as file:
        bot.send_document(id, file)


def send_to_developers(msg, file=False):
    for id in developer_chat_IDs:
        if id:
            if file:
                send_file(msg, id)
            else:
                bot.send_message(
                    id,
                    msg,
                )


#---------------------------------------------------------------------Bot_messages-----------------------------------------------------------------------------------------------------------------


# --- Help ---
@bot.message_handler(commands=["help"])
@error_handler
def error_command(message):
    print(message)
    bot.reply_to(
        message, templates["help.txt"],parse_mode='HTML'
    )  # finish here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@bot.message_handler(commands=["commands"])
@error_handler
def error_command(message):
    print(message)
    bot.reply_to(
        message, templates["commands.txt"],parse_mode='HTML'
    )  # finish here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# --- Tokens info ---
@bot.message_handler(commands=["tokens_info"])
@error_handler
def tokens_info_command(message):
    # bot.reply_to(message, templates["help.txt"])
    bot.reply_to(message, "Not implemented",parse_mode='HTML')


# --- About ---
@bot.message_handler(commands=["about", "start"])
@error_handler
def about_command(message):
    bot.reply_to(message, templates["description.txt"],parse_mode='HTML')


# --- Report bug ---
@bot.message_handler(commands=["report_bug"])
@error_handler
def report_bug_command(message):
    bot.reply_to(message, templates["report_bug.txt"],parse_mode='HTML')


# --- Request feature ---
@bot.message_handler(commands=["request_feature"])
@error_handler
def request_feature_command(message):
    bot.reply_to(message, templates["request_feature"],parse_mode='HTML')


# --- Enable ---
@bot.message_handler(commands=["enable"])
@error_handler
def enable_command(message):
    # logic
    bot.reply_to(message, templates["enabled.txt"],parse_mode='HTML')

    


# --- Disable ---
@bot.message_handler(commands=["disable"])
@error_handler
def handle_start(message):
    # logic
    bot.reply_to(message, templates["disabled.txt"],parse_mode='HTML')


# --- Set temp ---
@bot.message_handler(commands=["set_temperature"])
@error_handler
def set_temp_command(message):
    # logic (check val from 0 to 1!)
    bot.reply_to(message, "Not implemented",parse_mode='HTML')


# --- Handling new groups ---
@bot.message_handler(content_types=["new_chat_members"])
@error_handler
def handle_new_chat_members(message):
    for new_chat_member in message.new_chat_members:
        if new_chat_member.id == bot_id:
            bot.send_message(message.chat.id, templates["new_group_welcome.txt"],parse_mode='HTML')
            bot.send_message(
                message.chat.id, "Initializing..."
            )  # Will be replaced with sticker


#--------------------------GPT_Handlers--------------------------------------------------------------

@bot.message_handler(commands=['question_to_bot'])
@error_handler
def handle_start(message):
    
     bot.send_message(message.chat.id, gpt.question_to_bot(openAI_api_key,openAI_organization_key,message.text),parse_mode='HTML')





model = "gpt-3.5-turbo"
temporary_memory = []

@bot.message_handler(commands=["start_conservation"])
def about_command(message):

    full_message = message.text
    message_to_gpt = ''
    system_content = 'Have a dialogue, be a friendly helper'    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Can be changed!!!!!!!!!!!!!
    
    bot.send_message(message.chat.id, "Your conservation was started.\nIf you want to end it write\n/end_conservation",parse_mode='HTML')     #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Can be changed!!!!!!!!!!!!!!

    #Split the command /start and 'message after this' - message_to_gpt
    temporary_memory.append('/start')
    try:
        for i in range(full_message.index(' ')+1, len(full_message)):
            message_to_gpt = message_to_gpt + full_message[i]

        response = gpt.get_response(gpt.message_to_ai(openAI_api_key,openAI_organization_key,model,system_content,message_to_gpt))

        temporary_memory.append([message_to_gpt,response])

        bot.send_message(message.chat.id, response,parse_mode='HTML')

    except:
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')

    

@bot.message_handler(commands=["end_conservation"])
def about_command(message):
    bot.send_message(message.chat.id, "The conservation ended",parse_mode='HTML')     #!!!!!!!!!!!!!!!!!!!!!!!!!!!!Can be changed!!!!!!!!!!!!!!!!
    temporary_memory.clear()
    

@bot.message_handler(content_types='text')
def about_command(message):


    system_content = 'Have a dialogue, be a friendly helper'    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Can be changed!!!!!!!!!!!!!
    if '/start' in temporary_memory:                    
            
        response = gpt.get_response(gpt.conservation(openAI_api_key,openAI_organization_key,model,system_content,message.text,temporary_memory))

        temporary_memory.append([message.text,response])

        bot.send_message(message.chat.id, response,parse_mode='HTML')

    elif message.text[0] == '/':
        bot.reply_to(message, "Incorrect command.\n/help for list of messages")
        if'/start' in temporary_memory:
            bot.send_message(message.chat.id, 'Your conservation is still going',parse_mode='HTML')

    else:
        bot.send_message(message.chat.id, 'Out of conservation',parse_mode='HTML')
        



logger.info("Bot started")
bot.polling()
