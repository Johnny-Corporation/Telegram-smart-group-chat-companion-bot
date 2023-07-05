from dataclasses import dataclass
from telebot import TeleBot
from telebot.types import Message
from db_controller import Controller
import openai
from dotenv import load_dotenv
from os import environ
from datetime import datetime
from logging import Logger

load_dotenv(".env")

openAI_api_key = environ.get("OPENAI_API_KEY")
if not openAI_api_key:
    print("Failed to load OpenAI API key from environment, exiting...")
    exit()
openai.api_key = openAI_api_key

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
    """
    Args:
        id_ (int): chat id
        trigger_messages_count (int): sets the numbers of messages needed to trigger the bot in cycle.
        (eg: if set to 5, bot will read conversation each time after 5 new messages, only when there were no replies to bot's message)
        temporary_memory_size (int): sets number of messages given to GPT (eg: if set to 5, gpt will read only 5 last messages;
        This does not affect persistent memory! Persistent memory keeps whole conversation.)
    """

    def __post_init__(self):
        self.messages_history = []
        self.messages_count = 0  # incremented by one each message, think() function is called when hit trigger_messages_count
        self.enabled = False

    def think(self):
        """reads last"""

    def new_message(self, message: Message) -> str:
        if not self.enabled:
            return
        text = message.text
        db_controller.add_message_event(
            self.chat_id,
            text,
            datetime.now(),
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.username,
        )
        if len(self.messages_history) == self.temporary_memory_size:
            self.messages_history.pop(0)
            self.messages_history.append(text)

        self.messages_count += 1

        if (
            (self.messages_count == self.trigger_messages_count)
            or ("@" + self.bot_username in text)
            or (
                message.reply_to_message
                and message.reply_to_message.from_user.username == self.bot_username
            )
        ):
            self.messages_count = 0
            return "[GPT-answer]"

    def load_data(self):
        recent_events = db_controller.get_last_n_message_events_from_chat(
            self.chat_id, self.temporary_memory_size
        )
        if not recent_events:
            return
        self.messages_history = db_controller.get_last_n_messages_from_chat(
            self.chat_id, self.temporary_memory_size
        )


# TODO
# [ ] log events
# [ ] dynamically change trigger count
# [x] always reply when tagging or replying
# [ ] language change
# [ ] Add gpt
