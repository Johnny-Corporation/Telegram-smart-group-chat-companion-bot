from dataclasses import dataclass
from telebot import TeleBot
from telebot.types import Message
import soundfile as sf
from utils.db_controller import Controller
import utils.gpt_interface as gpt
from utils.time_tracking import *
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from random import random
from utils.functions import num_tokens_from_string, num_tokens_from_messages
from os import remove, makedirs

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from dateutil.relativedelta import relativedelta
from __main__ import *
from utils.functions import load_templates

templates = load_templates("templates\\")


load_dotenv(".env")


db_controller = Controller()


@dataclass
class Johnny:
    """Group handler, assumes to be created as separate instance for each chat"""

    bot: TeleBot
    templates
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

        #Permissions
        self.temporary_memory_size_limit = 20
        self.dynamic_gen_permission = False
        self.voice_output_permission = False
        self.sphere_permission = False
        self.temperature_permission = False
        self.frequency_penalty_permission = False
        self.presense_penalty_permission = False
        self.voice_input_permission = False


        #User 
        self.subscription = 'Free'
        self.tokens_limit = 100000
        self.allowed_groups = 1
        self.id_groups = []

        #Group
        self.owner_id = None


    def one_answer(self, message: Message, groups: dict):
        response = gpt.create_chat_completion(
            [message.text], reply=None, model=self.model
        )
        tokens_used = gpt.extract_tokens(response)
        self.total_spent_tokens[0] += tokens_used[0]
        self.total_spent_tokens[1] += tokens_used[1]

        if message.chat.id<0:
            groups[self.owner_id].total_spent_tokens[0] = self.total_spent_tokens[0]
            groups[self.owner_id].total_spent_tokens[1] = self.total_spent_tokens[1]
        return gpt.extract_text(response)

    def new_message(
        self,
        message: Message,
        groups: dict
    ) -> str:
        
        if len(groups[self.owner_id].id_groups) > groups[self.owner_id].allowed_groups:
            self.bot.send_message(message.chat.id, self.templates[self.lang_code]["exceed_limit_on_groups.txt"])

            groups[self.owner_id].id_groups.remove(message.chat.id)

            self.bot.leave_chat(message.chat.id)

        if message.content_type == 'voice' and self.voice_input_permission == True:

            file_name_full="output\\voice_in\\"+message.voice.file_id+".ogg"
            file_name_full_converted="output\\voice_in\\"+message.voice.file_id+".wav"
            file_info = self.bot.get_file(message.voice.file_id)


            makedirs("output\\voice_in", exist_ok=True)

            downloaded_file = self.bot.download_file(file_info.file_path)
            with open(file_name_full, 'wb') as new_file:
                new_file.write(downloaded_file)

            # Load ogg file
            data, samplerate = sf.read(file_name_full)

            # Export as wav
            sf.write(file_name_full_converted, data, samplerate)

            #Delete .ogg file
            remove(file_name_full)


            #text = gpt.speech_to_text(file_name_full_converted)

            self.bot.send_message(message.chat.id, text)

            #Delete .wav file
            remove(file_name_full_converted)


        else:
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
        

        if self.total_spent_tokens[0] + self.total_spent_tokens[1]>=self.tokens_limit:
            self.bot.send_message(message.chat.id, self.templates[self.lang_code]["exceed_limit_on_tokens.txt"])
            self.total_spent_tokens[0] = self.tokens_limit/2
            self.total_spent_tokens[1] = self.tokens_limit/2
            return
        elif groups[self.owner_id].total_spent_tokens[0] + groups[self.owner_id].total_spent_tokens[1]>=self.tokens_limit:
            self.bot.send_message(message.chat.id, self.templates[self.lang_code]["exceed_limit_on_tokens.txt"])
            groups[self.owner_id].total_spent_tokens[0] = self.tokens_limit/2
            groups[self.owner_id].total_spent_tokens[1] = self.tokens_limit/2
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

            if self.dynamic_gen and self.dynamic_gen_permission:
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


            if message.chat.id<0:
                groups[self.owner_id].total_spent_tokens[0] = self.total_spent_tokens[0]
                groups[self.owner_id].total_spent_tokens[1] = self.total_spent_tokens[1]

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


    def add_new_user(
        self,
        chat_id,
        first_name,
        last_name,
        username,
        type_of_subscription: str,
        num_allowed_groups: int,
        temp_memory_size_limit: int,
        tokens_total: int,
        dynamic_generation: bool,
        voice_input: bool,
        voice_output: bool,
        sphere_context: bool,
        temperature: bool,
        freq_penalty: bool,
        presense_penalty: bool,

    ):

        # get current date
        current_date = datetime.now().isoformat()


        if db_controller.check_the_existing_of_user_with_sub(int(chat_id)):
            db_controller.delete_the_existing_of_user_with_sub(int(chat_id))

        db_controller.add_user_with_sub(
            chat_id, 
            type_of_subscription,
            num_allowed_groups,
            temp_memory_size_limit,
            current_date,
            first_name,
            str(last_name),
            username,
            tokens_total,
            dynamic_generation,
            voice_input,
            voice_output,
            sphere_context,
            temperature,
            freq_penalty,
            presense_penalty
        )

        if type_of_subscription != 'Free':

            self.bot.send_message(chat_id, self.templates[self.lang_code]["new_subscriber.txt"].format(sub=self.subscription), parse_mode="HTML")

        


    def extend_sub(self, chat_id, first_name, last_name, username):

        date_of_start_txt = db_controller.get_last_date_of_start_of_user(chat_id)
        prev_date_of_start = datetime.fromisoformat(date_of_start_txt) + relativedelta(months=1)
        date_of_start = prev_date_of_start.isoformat()

        db_controller.add_user_with_sub(
            chat_id, 
            self.subscription,
            self.allowed_groups,
            self.temporary_memory_size_limit,
            date_of_start,
            first_name,
            str(last_name),
            username,
            self.tokens_limit,
            self.dynamic_gen_permission,
            self.voice_input_permission,
            self.voice_output_permission,
            self.sphere_permission,
            self.temperature_permission,
            self.frequency_penalty_permission,
            self.presense_penalty_permission
        )

        self.bot.send_message(chat_id, self.templates[self.lang_code]["sub_extend.txt"].format(sub=self.subscription), parse_mode="HTML")

        def sub_tracking(chat_id, date_of_start):

            #Add reminders!!!
            db_controller.delete_the_existing_of_user_with_sub_by_date(date_of_start)

            current_date = datetime.now().isoformat()

            check = db_controller.check_the_existing_of_user_with_sub(chat_id)
                
            if check == False:

                self.bot.send_message(chat_id, self.templates[self.lang_code]["sub_was_end.txt"], parse_mode="HTML")

                db_controller.add_user_with_sub(
                    chat_id, 
                    "Free",
                    1,
                    20,
                    current_date,
                    " ",
                    " ",
                    " ",
                    100000,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False
                )

                self.subscription = "Free"
                self.allowed_groups = 1
                self.tokens_limit = 100000
                self.dynamic_gen_permission = False
                self.voice_input_permission = False
                self.voice_output_permission = False
                self.sphere_permission = False
                self.temperature_permission = False
                self.frequency_penalty_permission = False
                self.presense_penalty_permission = False
                self.temporary_memory_size_limit = 20

                self.temperature = 1
                self.frequency_penalty = 0.2
                self.presense_penalty = 0.2
                self.sphere = ""
                self.temporary_memory_size = 20

            self.bot.send_message(chat_id, self.templates[self.lang_code]["sub_was_end_with_extend.txt"].format(sub=self.subscription), parse_mode="HTML")

            

        # create a scheduler
        sub_scheduler = BackgroundScheduler()

        # schedule a task to print a number after 2 seconds
        sub_scheduler.add_job(sub_tracking, 'date', run_date=prev_date_of_start + relativedelta(months=1), args=[chat_id, date_of_start], misfire_grace_time=86400)

        # start the scheduler
        sub_scheduler.start()

        

        
    def track_sub(self, chat_id, new):
        
        if self.subscription != "Free":

            def sub_tracking(chat_id, date_of_start):

                #Add reminders!!!
                db_controller.delete_the_existing_of_user_with_sub_by_date(date_of_start)

                current_date = datetime.now().isoformat()

                check = db_controller.check_the_existing_of_user_with_sub(chat_id)

                if not check:

                    self.bot.send_message(chat_id, self.templates[self.lang_code]["sub_was_end.txt"], parse_mode="HTML")

                    db_controller.add_user_with_sub(
                        chat_id, 
                        "Free",
                        1,
                        20,
                        current_date,
                        " ",
                        " ",
                        " ",
                        100000,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False
                    )

                    self.subscription = "Free"
                    self.allowed_groups = 1
                    self.tokens_limit = 100000
                    self.dynamic_gen_permission = False
                    self.voice_input_permission = False
                    self.voice_output_permission = False
                    self.sphere_permission = False
                    self.temperature_permission = False
                    self.frequency_penalty_permission = False
                    self.presense_penalty_permission = False
                    self.temporary_memory_size_limit = 20

                    self.temperature = 1
                    self.frequency_penalty = 0.2
                    self.presense_penalty = 0.2
                    self.sphere = ""
                    self.temporary_memory_size = 20

                self.bot.send_message(chat_id, self.templates[self.lang_code]["sub_was_end_with_extend.txt"].format(sub=self.subscription), parse_mode="HTML")

            if new == True:
                start_date_txt = db_controller.get_last_date_of_start_of_user(chat_id)
                start_date = datetime.fromisoformat(start_date_txt)

                # create a scheduler
                sub_scheduler = BackgroundScheduler()

                # schedule a task to print a number after 2 seconds
                sub_scheduler.add_job(sub_tracking, 'date', run_date=start_date + relativedelta(months=1), args=[chat_id, start_date_txt], misfire_grace_time=86400)

                # start the scheduler
                sub_scheduler.start()
            else:
                all_dates = db_controller.get_users_with_sub_by_chat_id(chat_id)

                for date in all_dates:
                    start_date_txt = date[0]
                    start_date = datetime.fromisoformat(start_date_txt)
                    
                    # create a scheduler
                    sub_scheduler = BackgroundScheduler()

                    # schedule a task to print a number after 2 seconds
                    sub_scheduler.add_job(sub_tracking, 'date', run_date=start_date + relativedelta(months=1), args=[chat_id, start_date_txt], misfire_grace_time=86400)

                    # start the scheduler
                    sub_scheduler.start()

    def change_owner_of_group(self, username):

        new_user = db_controller.get_user_with_sub_by_username(username) 

        return new_user

    def add_purchase_of_tokens(self, chat_id, num_of_new_tokens):
        new_total_tokens = self.tokens_limit + num_of_new_tokens
        db_controller.update_tokens_of_user_with_sub(chat_id, new_total_tokens)


    def change_memory_size(self, size):
        self.temporary_memory_size = size
        self.messages_history = []
        self.load_data()


    def load_subscription(self, chat_id):
        data = db_controller.get_user_with_sub_by_chat_id(chat_id)

        if data != {}:
            self.subscription = data["TypeOfSubscription"]
            self.allowed_groups = data["NumAllowedGroups"]
            self.tokens_limit = data["TokensTotal"]
            self.dynamic_gen_permission = data["DYNAMIC_GENERATION"]
            self.voice_input_permission = data["VOICE_INPUT"]
            self.voice_output_permission = data["VOICE_OUTPUT"]
            self.sphere_permission = data["SphereContext"]
            self.temperature_permission = data["Temperature"]
            self.frequency_penalty_permission = data["FrequencyPenalty"]
            self.presense_penalty_permission = data["PresensePenalty"]
            self.temporary_memory_size_limit = data["TemporaryMemorySize"]
            self.owner_id = chat_id
            return True
        return False



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
# [ ] document read

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

# [ ] TypeError fix
# [ ] QIWI payment
# [ ] KickStarted
# [ ] BoomStarted


# [ ] Command to change group's owner
# [ ] Detect the developers in initializations
# [ ] english templates to other languages