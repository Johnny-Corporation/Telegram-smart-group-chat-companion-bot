from dataclasses import dataclass
from telebot import TeleBot
from telebot.types import Message
from utils.db_controller import Controller
import utils.gpt_interface as gpt
from dotenv import load_dotenv
from datetime import datetime
from random import random
from utils.functions import num_tokens_from_string, num_tokens_from_messages

load_dotenv(".env")


db_controller = Controller()


@dataclass
class Johnny:
    """Group handler, assumes to be created as separate instance for each chat"""

    bot: TeleBot
    chat_id: int
    bot_username: str
    temporary_memory_size: int = 20
    language_code: str = "eng"
    trigger_probability: float = 0.2
    model = "gpt-3.5-turbo"
    temperature: float = 1
    frequency_penalty: float = 0.2
    presense_penalty: float = 0.2
    answer_length: str = "as you need"
    sphere: str = ""
    system_content: str = ""
    """
    Args:
        id_ (int): chat id
        trigger_messages_count (int): sets the numbers of messages needed to trigger the bot in cycle.
        (eg: if set to 5, bot will read conversation each time after 5 new messages, only when there were no replies to bot's message)
        temporary_memory_size (int): sets number of messages given to GPT (eg: if set to 5, gpt will read only 5 last messages;
        This does not affect persistent memory! Persistent memory keeps whole conversation.)
        language_code (str): Language
        random_trigger (bool) If set to True, bot triggers randomly. When enabled, trigger_messages_count is ignored
        random_trigger_probability (float from 0 to 1) = Triggering probability on each message. Works only when random trigger is True 
        temperature (float) temperature value, used in requests to GPT

        system_content (str) it includes. "answer_length". "spheres of conservation". "user_requests".
        
    """

    def __post_init__(self):
        # list of lists, where each list follows format: [senders_name, text]
        self.messages_history = []
        self.messages_count = 0  # incremented by one each message, think() function is called when hit trigger_messages_count
        self.lang_code = None
        self.enabled = False
        self.total_spent_tokens = [0, 0]  # prompt and completion tokens
        self.dynamic_gen = False
        self.dynamic_gen_chunks_frequency = 30  # when dynamic generation is enabled, this value controls how often to edit telegram message, for example when set to 3, message will be updated each 3 chunks from OpenAI API stream

    def one_answer(self, message: Message):
        response = gpt.create_chat_completion(
            [message.text], reply=None, model=self.model
        )
        tokens_used = gpt.extract_tokens(response)
        self.total_spent_tokens[0] += tokens_used[0]
        self.total_spent_tokens[1] += tokens_used[1]
        return gpt.extract_text(response)

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
            self.total_spent_tokens[0],
            self.total_spent_tokens[1],
        )

        self.messages_history.append([message.from_user.first_name, text])

        if len(self.messages_history) == self.temporary_memory_size:
            self.messages_history.pop(0)

        if not self.enabled:
            return

        if (
            ("@" + self.bot_username in text)
            or (
                message.reply_to_message
                and message.reply_to_message.from_user.username == self.bot_username
            )
            or (random() < self.trigger_probability)
        ):
            response = gpt.create_chat_completion(
                self.messages_history,
                reply=bool(message.reply_to_message),
                answer_length=self.answer_length,
                model=self.model,
                temperature=self.temperature,
                stream=self.dynamic_gen,
                frequency_penalty=self.frequency_penalty,
                presense_penalty=self.presense_penalty,
            )

            if self.dynamic_gen:
                text_answer = ""  # stores whole answer
                bot_message = self.bot.send_message(
                    message.chat.id, "Thinking...", parse_mode="Markdown"
                )

                update_count = 1
                for i in response:
                    if ("content" in i["choices"][0]["delta"]) and (
                        text_chunk := i["choices"][0]["delta"]["content"]
                    ):
                        text_answer += text_chunk
                        update_count += 1

                        if update_count == self.dynamic_gen_chunks_frequency:
                            update_count = 0
                            self.bot.edit_message_text(
                                chat_id=message.chat.id,
                                message_id=bot_message.message_id,
                                text=text_answer,
                            )

                self.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=bot_message.message_id,
                    text=text_answer,
                )

                # counting tokens
                self.total_spent_tokens[0] += num_tokens_from_string(text_answer)
                self.total_spent_tokens[1] += num_tokens_from_messages(
                    gpt.get_messages_in_official_format(self.messages_history),
                    model=self.model,
                )

            else:
                text_answer = gpt.extract_text(response)

                # Checking context understating
                if (
                    (self.trigger_probability != 1)
                    and (self.trigger_probability != 0)
                    and (not gpt.check_context_understanding(text_answer))
                ):
                    return
                # Checking model answer is about selected sphere
                if (
                    (self.trigger_probability != 1)
                    and (self.trigger_probability != 0)
                    and (self.sphere)
                    and (not gpt.check_theme_context(text_answer, self.sphere))
                ):
                    return

                self.total_spent_tokens[0] += gpt.extract_tokens(response)[0]
                self.total_spent_tokens[1] += gpt.extract_tokens(response)[1]

                # If message was a reply to bot message, bot will reply to reply
                self.bot.send_message(
                    message.chat.id, text_answer, parse_mode="Markdown"
                )

            # Adding GPT answer to db and messages_history
            db_controller.add_message_event(
                self.chat_id,
                text_answer,
                datetime.now(),
                "JOHNNYBOT",
                "JOHNNYBOT",
                self.bot_username,
                self.total_spent_tokens[0],
                self.total_spent_tokens[1],
            )
            self.messages_history.append(["assistant", text_answer])

    def change_memory_size(self, size):
        self.temporary_memory_size = size
        self.messages_history = []
        self.load_data()

    def load_data(self) -> None:
        """Loads data from to object from db"""
        recent_events = db_controller.get_last_n_message_events_from_chat(
            self.chat_id, self.temporary_memory_size
        )
        if not recent_events:
            return
        self.messages_history = db_controller.get_last_n_messages_from_chat(
            self.chat_id, self.temporary_memory_size
        )[::-1]
        for i in recent_events:
            if i[5] == "JOHNNYBOT":
                self.total_spent_tokens[0] = i[-2]
                self.total_spent_tokens[1] = i[-1]
                break


# TODO
# [x] log events
# [x] always reply when tagging or replying
# [x] language change
# [x] Add gpt
# [x] Count tokens
# [x] Ask question to bot (via reply)
# [x] test adding to group
# [x] dynamic generation
# [x] write input output tokens to db
# [x] refactoring
# [x] help command, all commands with descriptions <<---------Misha
# [x] Convert templates with parse_html<<---------- Misha
# [x] Make support for german and spanish
# [x] Make sticker support only for ru
# [x] Configure gpt for correct answers
# [x] manual mode <<--------------- Misha
# [x] Assistant; User in messages history (refactor temporary memory)
# [x] Dialog mode <<------ Misha
# [ ] translate all templates <<------ Misha
# [x] interface of changing all parameters + customization
# [x] account info command\
# [x] conservations in private messages
# [x] /start fix
# [x] functions set presense + frequency penalties

# ------------ for today (11 july 23) -------------
# [x] fix dynamic generation
# [x] assign name to messages
# [x] Make GPT answer no, when it doesnt understand context
# [x] Generate system_content (maybe add some system contents) <<--------- Misha
# [x] run on sfedu
# [x] add to our group

#  ----------- later -----------
# [x] Count tokens for dynamic generation via tokenizer <<-----------Misha
# [x] add all params like penalty max_tokens etc

# ------------ future features ---------
# [ ] Internet access parameter
# [ ] Audio messages support (maybe do one of element of customization)
# [ ] games with gpt (entertainment part)
# [ ] gpt answers to message by sticker or emoji
# [ ] activation keys for discount
# [x] conservations in private messages
# [ ] automatic calling functions
# [ ] automatic commands detection

# for today (11 july 23)
# [x] add commands for developers
# [x] db operations
# [x] Maybe add to TODO
# [x] get logs
# [x] separate logs

# --- for matvey in train ---
# [x] separate commands in files
# [x] fix clients info saving
# [ ] db for subs
# [x] commands for developers


# [x] tests
# [x] new private init file
# [x]

# [x]  fix dynamic generation
# [ ] internet access
# [ ] speech to text

# [ ] Fix templates, rephrase strange texts


# [ ] Run on server
