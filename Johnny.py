from dataclasses import dataclass
from telebot import TeleBot
from telebot.types import Message
from db_controller import Controller
import gpt_interface as gpt
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(".env")


db_controller = Controller()


@dataclass
class Johnny:
    """Group handler, assumes to be created as separate instance for each chat"""

    bot: TeleBot
    chat_id: int
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
        self.lang_code = None
        self.enabled = False
        self.total_spent_tokens = 0
        self.prompt_completion_tokens = [0, 0]
        self.dynamic_gen = True

    def think(self):
        """reads last"""

    def one_answer(self, message: Message):
        answer = gpt.one_question(message.text)
        self.total_spent_tokens += gpt.get_tokens(answer)[0] + gpt.get_tokens(answer)[1]
        self.new_message(message)
        return gpt.get_text(answer)

    def new_message(
        self,
        message: Message,
    ) -> str:
        text = message.text
        db_controller.add_message_event(
            self.chat_id,
            text,
            datetime.now(),
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.username,
        )
        self.messages_history.append(text)
        if len(self.messages_history) == self.temporary_memory_size:
            self.messages_history.pop(0)

        if not self.enabled:
            return

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

            gpt_answer = gpt.gpt_answer(
                self.messages_history, bool(message.reply_to_message)
            )

            self.total_spent_tokens += (
                gpt.get_tokens(gpt_answer)[0] + gpt.get_tokens(gpt_answer)[1]
            )

            self.prompt_completion_tokens[0] = (
                self.prompt_completion_tokens[0] + gpt.get_tokens(gpt_answer)[0]
            )
            self.prompt_completion_tokens[1] = (
                self.prompt_completion_tokens[1] + gpt.get_tokens(gpt_answer)[1]
            )

            db_controller.add_message_event(
                self.chat_id,
                gpt.get_text(gpt_answer),
                datetime.now(),
                "JOHNNYBOT",
                "JOHNNYBOT",
                self.bot_username,
                self.total_spent_tokens,
            )
            self.messages_history.append(gpt.get_text(gpt_answer))
            return gpt.get_text(gpt_answer)

    def load_data(self):
        recent_events = db_controller.get_last_n_message_events_from_chat(
            self.chat_id, self.temporary_memory_size
        )
        if not recent_events:
            return
        self.messages_history = db_controller.get_last_n_messages_from_chat(
            self.chat_id, self.temporary_memory_size
        )
        for i in recent_events[::-1]:
            if i[5] == "JOHNNYBOT":
                self.total_spent_tokens = i[-1]
                break


# TODO
# [x] log events
# [ ] dynamically change trigger count
# [x] always reply when tagging or replying
# [x] language change
# [x] Add gpt
# [x] Count tokens
# [x] Ask question to bot (via reply)
# [x] test adding to group
# [ ] dynamic generation
# [ ] Readme for gh    <<---------- Misha
# [ ] Internet access parameter
# [ ] write input output tokens to db
# [ ] refactoring
# [ ] in question_to_bot make bot react to both ways: reply and in one message with command <<---------- Misha
# [ ] help command, all commands with descriptions <<---------Misha
# [ ] Convert templates with parse_html<<---------- Misha
# [ ] Connect payment system <<---------- Misha
# [ ] Make support for german and spanish
# [ ] Make sticker support only for ru
