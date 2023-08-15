from dataclasses import dataclass
from telebot import TeleBot
from telebot.types import Message
from utils.db_controller import Controller
import utils.gpt_interface as gpt
from dotenv import load_dotenv
from datetime import datetime
from random import random
import json
from utils.functions import get_file_content, describe_image
from os import environ

load_dotenv(".env")


db_controller = Controller()

functions_waiting_messages = {
    "google": "Googling question '{}'",
    "read_from_link": "Reading content from link {}",
    "generate_image": "Generating image(s) with prompt '{}'",
}


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
    presence_penalty: float = 0.2
    answer_length: str = "as you need"
    sphere: str = ""
    system_content: str = ""
    allow_functions: bool = True

    def __post_init__(self):
        # list of lists, where each list follows format: [senders_name, text]
        self.messages_history = []
        self.lang_code = None
        self.enabled = False
        self.dynamic_gen = True
        # Needed to store requested links and restrict repeating useless requests
        self.dynamic_gen_chunks_frequency = 30  # when dynamic generation is enabled, this value controls how often to edit telegram message, for example when set to 3, message will be updated each 3 chunks from OpenAI API stream
        self.last_function_request = None

    def get_completion(self, allow_function_call=None):
        """Returns completion object and takes one time arguments."""
        return gpt.create_chat_completion(
            self.messages_history,
            reply=bool(self.message.reply_to_message),
            answer_length=self.answer_length,
            model=self.model,
            temperature=self.temperature,
            stream=self.dynamic_gen,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            use_functions=(
                self.allow_functions
                if allow_function_call is None
                else allow_function_call
            ),
        )

    def one_answer(self, message: Message):
        response = gpt.create_chat_completion(
            [message.text], reply=None, model=self.model, stream=self.dynamic_gen
        )
        return gpt.extract_text(response)

    def new_message(
        self,
        message: Message,
    ):
        match message.content_type:
            case "document":
                text = "[FILE] Content:" + get_file_content(self.bot, message)
            case "photo":
                image_info = self.bot.get_file(message.photo[-1].file_id)
                image_url = f"https://api.telegram.org/file/bot{environ['BOT_API_TOKEN']}/{image_info.file_path}"
                text = "[IMAGE] Description:" + describe_image(image_url)
            case "text":
                text = message.text
            case _:
                return  # unsupported event type
        db_controller.add_message_event(
            self.chat_id,
            text,
            datetime.now(),
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.username,
        )
        self.message = message
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
            # --- GPT answer generation ---

            self.response = self.get_completion()

            text_answer = (
                self.dynamic_generation(self.response)
                if self.dynamic_gen
                else self.static_generation(self.response)
            )

            # Adding GPT answer to db and messages_history
            db_controller.add_message_event(
                self.chat_id,
                str(text_answer),
                datetime.now(),
                "$BOT$",
                "$BOT$",
                self.bot_username,
            )

            self.messages_history.append(["$BOT$", text_answer])

    def static_generation(self, completion):
        """Takes completion object and returns text answer. Handles message in telegram"""

        # Check function call
        response_message = completion["choices"][0]["message"]

        if response_message.get("function_call"):
            function_name = response_message["function_call"]["name"]
            function_args = json.loads(response_message["function_call"]["arguments"])
            argument = next(iter(function_args.values()))

            self.bot.send_message(
                self.message.chat.id,
                functions_waiting_messages[function_name].format(argument),
                disable_web_page_preview=True,
            )

            # If this response is same as previous, do not allow function call in next request and notify user
            if self.last_function_request == (function_name, function_args):
                self.bot.send_message(
                    self.message.chat.id,
                    "Can't find needed data. (Function call failed)",
                )
                self.last_function_request = None
                return self.static_generation(
                    self.get_completion(allow_function_call=False)
                )

            self.last_function_request = (function_name, function_args)

            # Additional arguments
            additional_args = {}
            if function_name == "generate_image":
                additional_args = {"bot": self.bot, "chat_id": self.chat_id}

            # Saving function result to history
            self.messages_history.append(
                [
                    "$FUNCTION$",
                    gpt.get_official_function_response(
                        function_name, function_args, additional_args=additional_args
                    ),
                ]
            )

            if function_name == "generate_image":
                return "[IMAGES]"  # this will be saved as bot message in history
            return self.static_generation(self.get_completion())

        self.response = completion
        text_answer = gpt.extract_text(self.response)
        # Check context understanding
        if not self.check_understanding(text_answer):
            return None

        self.bot.send_message(self.message.chat.id, text_answer, parse_mode="Markdown")
        return text_answer

    def dynamic_generation(self, completion):
        """Takes completion object and returns text answer. Handles message in telegram"""

        if self.last_function_request is None:
            self.thinking_message = self.bot.send_message(
                self.chat_id, "🤔", parse_mode="Markdown"
            )

        text_answer = ""  # stores whole answer

        update_count = 1
        func_call = {
            "name": None,
            "arguments": "",
        }

        for res in completion:
            delta = res.choices[0].delta
            if "function_call" in delta:
                if "name" in delta.function_call:
                    func_call["name"] = delta.function_call["name"]
                if "arguments" in delta.function_call:
                    func_call["arguments"] += delta.function_call["arguments"]
            if res.choices[0].finish_reason == "function_call":
                # Handling function call

                function_name = func_call["name"]
                function_args = json.loads(func_call["arguments"])
                argument = next(iter(function_args.values()))

                self.bot.send_message(
                    self.message.chat.id,
                    functions_waiting_messages[function_name].format(argument),
                    disable_web_page_preview=True,
                )

                # If previous function call was the same as current
                if self.last_function_request == (function_name, function_args):
                    self.bot.send_message(
                        self.message.chat.id,
                        "Can't find needed data. (Function call failed)",
                    )
                    self.last_function_request = None
                    return self.dynamic_generation(
                        self.get_completion(allow_function_call=False)
                    )

                self.last_function_request = (function_name, function_args)

                # Additional arguments
                additional_args = {}
                if function_name == "generate_image":
                    additional_args = {"bot": self.bot, "chat_id": self.chat_id}

                # Saving function result to history
                self.messages_history.append(
                    [
                        "$FUNCTION$",
                        gpt.get_official_function_response(
                            function_name,
                            function_args,
                            additional_args=additional_args,
                        ),
                    ]
                )

                if function_name == "generate_image":
                    return "[IMAGES]"  # this will be saved as bot message in history
                return self.dynamic_generation(self.get_completion())
                # End of handling function call

            if ("content" in res["choices"][0]["delta"]) and (
                text_chunk := res["choices"][0]["delta"]["content"]
            ):
                text_answer += text_chunk
                update_count += 1

                if update_count == self.dynamic_gen_chunks_frequency:
                    update_count = 0
                    self.bot.edit_message_text(
                        chat_id=self.message.chat.id,
                        message_id=self.thinking_message.message_id,
                        text=text_answer,
                    )

        if update_count != 0:
            self.bot.edit_message_text(
                chat_id=self.message.chat.id,
                message_id=self.thinking_message.message_id,
                text=text_answer,
            )
        return text_answer

    def check_understanding(self, text_answer: str) -> bool:
        """Checks if GPT understands context of the question"""

        # Checking context understating
        if (
            (self.trigger_probability != 1)
            and (self.trigger_probability != 0)
            and (not gpt.check_context_understanding(text_answer))
        ):
            return False

        # Checking model answer is about selected sphere
        if (
            (self.trigger_probability != 1)
            and (self.trigger_probability != 0)
            and (self.sphere)
            and (not gpt.check_theme_context(text_answer, self.sphere))
        ):
            return False
        # Count tokens !!!!
        return True

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
# [x] Internet access parameter
# [x] Audio messages support (maybe do one of element of customization)
# [ ] games with gpt (entertainment part)
# [ ] gpt answers to message by sticker or emoji
# [x] activation keys for discount
# [x] conservations in private messages
# [x] automatic calling functions
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
# [x] db for subs
# [x] commands for developers


# [x] tests
# [x] new private init file
# [x]

# [x]  fix dynamic generation
# [ ] internet access
# [ ] speech to text

# [ ] Fix templates, rephrase strange texts


# [ ] Run on server
# [ ] Check parse mode md after editing message

# [ ] Check length and history len when it bigger
