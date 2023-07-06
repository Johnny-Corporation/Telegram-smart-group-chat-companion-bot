from dataclasses import dataclass
from telebot import TeleBot
from telebot.types import Message
from db_controller import Controller
import gpt_functions as gpt
import openai

from dotenv import load_dotenv
from os import environ
from datetime import datetime
from logging import Logger


load_dotenv(".env")

gpt_token = environ.get("OPENAI_API_KEY")
organization_token = environ.get("OPENAI_ORGANIZATION")

model = "gpt-3.5-turbo"

if not gpt_token:
    print("Failed to load OpenAI API key from environment, exiting...")
    exit()
if not organization_token:
    print("Failed to load Organization key from environment, exiting...")


openai.api_key = gpt_token     # !!!!!!!Don't sure!!!!!!!!!!

db_controller = Controller()


@dataclass
class Johnny:
    """Group handler, assumes to be created as separate instance for each chat"""

    bot: TeleBot
    chat_id: int
    logger: Logger
    bot_username: str
    trigger_messages_count: int = 5
    temporary_memory_size: int = 30
    allow_dynamically_change_message_trigger_count: bool = True
    language_code: str = "eng"
    gpt_token: str = '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'
    organization_token: str = 'org-pQuAcA9nvf69dTMuXLO1cRNo'
    model: str = 'gpt-3.5-turbo'

    """
    Args:
        id_ (int): chat id
        trigger_messages_count (int): sets the numbers of messages needed to trigger the bot in cycle.
        (eg: if set to 5, bot will read conversation each time after 5 new messages, only when there were no replies to bot's message)
        temporary_memory_size (int): sets number of messages given to GPT (eg: if set to 5, gpt will read only 5 last messages;
        This does not affect persistent memory! Persistent memory keeps whole conversation.)
    """

    def __post_init__(self):
        self.temporary_memory = []
        self.messages_count = 0  # incremented by one each message, think() function is called when hit trigger_messages_count
        self.enabled = False
        self.dialog_enabled = False
        self.qustion_enabled = False

    # def read_last(self):
    #     """reads last"""


    # --- gpt answer in automatic mode ---
    def new_message(self, message: Message) -> str:
        


        # --- check the turning on the automode ---
        if not self.enabled:
            return 
        
        # # --- add messages to database ---
        text = message.text
        # db_controller.add_message_event(
        #     self.chat_id,
        #     text,
        #     datetime.now(),
        #     message.from_user.first_name,
        #     message.from_user.last_name,
        #     message.from_user.username,
        # )

        # --------- Work with temporary memory ---------

        self.temporary_memory.append(text)

        # --- checking the step up of temporary memory ---
        if len(self.temporary_memory) == self.temporary_memory_size:
            self.temporary_memory.pop(0)
            self.temporary_memory.append(text)

        self.messages_count += 1

        # --- Automode handlers ---
        if (
            (self.messages_count == self.trigger_messages_count)
            or ("@" + self.bot_username in text)
        ):
            
            self.messages_count = 0
            return gpt.get_response(gpt.automode(self.gpt_token, self.organization_token, self.model, self.temporary_memory))         #!!!!!!!!!!!!!!!!Do!!!!!!!!!!!!!!!!!!!!!!
        
        if (
                message.reply_to_message
                and message.reply_to_message.from_user.username == self.bot_username
            ):
            
            return gpt.get_response(gpt.reply_to_message(self.gpt_token, self.organization_token, self.model, self.temporary_memory))


    def load_data(self):
        recent_events = db_controller.get_last_n_message_events_from_chat(
            self.chat_id, self.temporary_memory_size
        )
        if not recent_events:
            return
        self.temporary_memory = db_controller.get_last_n_messages_from_chat(
            self.chat_id, self.temporary_memory_size
        )


# TODO
# [ ] log events
# [ ] dynamically change trigger count
# [x] always reply when tagging or replying
# [ ] language change
# [ ] Add gpt
