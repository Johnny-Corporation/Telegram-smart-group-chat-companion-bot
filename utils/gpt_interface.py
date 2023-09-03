import openai
from os import environ, path, listdir
from utils.logger import logger  # needed for hidden logs, do not remove
import utils.functions as functions
import json
from utils.internet_access import *
from time import sleep
import replicate


# Cant import from functions because og the cycle imports
def load_templates(dir: str) -> dict:
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


templates = load_templates("templates\\")

openAI_api_key = environ.get("OPENAI_API_KEY")
if not openAI_api_key:
    print("Failed to load OpenAI API key from environment, exiting...")
    exit()
openai.api_key = openAI_api_key


def extract_text(completion: openai.ChatCompletion) -> str:
    """Extracts text from OpenAI API response"""
    if hasattr(completion, "choices"):
        return completion.choices[0].message.content
    else:
        result = ""
        for i in completion:
            result += i
        return result


def check_function_call(completion: openai.ChatCompletion) -> bool:
    return bool(completion["choices"][0]["message"].get("function_call"))


def extract_function_call_details(completion: openai.ChatCompletion) -> dict:
    return {
        "name": completion["choices"][0]["message"]["function_call"]["name"],
        "args": json.loads(
            completion["choices"][0]["message"]["function_call"]["arguments"]
        ),
    }


def get_messages_in_official_format(messages):
    """Converts messages kept in Johnny to official format"""
    previous_messages = []
    for m in messages:
        if m[0] == "$FUNCTION$":
            previous_messages.append(m[1])
            continue
        previous_messages.append(
            {
                "role": ("assistant" if m[0] == "$BOT$" else "user"),
                "content": m[1],
                "name": functions.remove_utf8_chars(m[0]),
            }
        )
    return previous_messages


def build_prompt_for_lama(messages):
    lama_prompt = ""
    for m in messages:
        if m[0] == "$BOT$":
            lama_prompt += f"LAMA: {m[1]}"
        else:
            lama_prompt += f"{m[0]}: {m[1]}"
        lama_prompt += "\n"
    lama_prompt += "LAMA: "
    return lama_prompt


def generate_image_dalle(prompt, n, size):
    """Returns links to image"""
    response = openai.Image.create(prompt=prompt, n=n, size=size)
    links = []
    for i in response["data"]:
        links.append(i["url"])
    return links


def get_lama_answer(
    prompt,
    system_prompt="You are a helpful assistant.",
    temperature=0.9,
    top_p=0.5,
    max_tokens=1024,
):
    output = replicate.run(
        "replicate/llama-2-70b-chat:2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf",
        input={
            "prompt": prompt,
            "system_prompt": system_prompt,
            "temperature": temperature,
            "top_p": top_p,
            "max_new_tokens": max_tokens,
        },
    )

    return output


def create_chat_completion(
    johnny,  # for resetting memory in when server error
    messages: list,
    lang: str = "en",
    system_content: str = None,
    answer_length: int = "short",
    use_functions: bool = False,
    reply: bool = False,  # SYS
    model: str = "gpt-3.5-turbo",
    temperature: int = 0.5,
    top_p: float = 1,
    n: int = 1,
    stream: bool = False,
    stop: str = None,
    frequency_penalty: float = 0,
    presence_penalty: float = 0,
) -> openai.ChatCompletion:
    """Creates ChatCompletion
    messages(list): list of dicts, where key is users name and value is his message
    reply(bool): True means GPT will consider last message, False means not, None means system input field will be empty
    """

    # --- Building system content ---
    # system_content = ""
    system_content = f"You are a telegram bot named Johnny, developed by JohnnyCorp team. Your answers should be {answer_length}, use emojis."

    previous_messages = [
        {
            "role": "system",
            "content": system_content,
        }
    ]

    # --- Building messages ---

    previous_messages.extend(get_messages_in_official_format(messages))

    # --- Creating ChatCompletion object ---

    chat_completion_arguments = {
        "model": model,
        "messages": previous_messages,
        "temperature": temperature,
        "top_p": top_p,
        "n": n,
        "stream": stream,
        "stop": stop,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
    }
    if use_functions:
        chat_completion_arguments["functions"] = gpt_functions_description
        chat_completion_arguments["function_call"] = "auto"

    try:
        if (model == "lama") or (model == "vicuna"):
            lama_prompt = build_prompt_for_lama(messages)
            completion = get_lama_answer(
                lama_prompt,
                system_prompt=system_content,
                temperature=temperature,
                top_p=top_p,
            )
            logger.info(f"Lama response:{completion}")
        else:
            logger.info("Requesting gpt...")
            completion = openai.ChatCompletion.create(**chat_completion_arguments)
    except openai.error.APIError as e:
        logger.error(f"OpenAI API returned an API Error: {e}")
        functions.send_to_developers(
            "❗❗Server error occurred❗❗ Using Lama without functions",
            johnny.bot,
            environ["DEVELOPER_CHAT_IDS"].split(","),
        )
        # johnny.messages_history = johnny.messages_history[-3:]
        # previous_messages = [
        #     {
        #         "role": "system",
        #         "content": system_content,
        #     }
        # ]
        # previous_messages.extend(
        #     get_messages_in_official_format(johnny.messages_history)
        # )
        # chat_completion_arguments = {
        #     "model": model,
        #     "messages": previous_messages,
        #     "temperature": temperature,
        #     "top_p": top_p,
        #     "n": n,
        #     "stream": stream,
        #     "stop": stop,
        #     "frequency_penalty": frequency_penalty,
        #     "presence_penalty": presence_penalty,
        # }
        # if use_functions:
        #     chat_completion_arguments["functions"] = gpt_functions_description
        #     chat_completion_arguments["function_call"] = "auto"
        # sleep(5)

        lama_prompt = build_prompt_for_lama(messages)
        completion = get_lama_answer(
            lama_prompt,
            system_prompt=system_content,
            temperature=temperature,
            top_p=top_p,
        )
        logger.info(f"Lama response:{completion}")

    except openai.error.APIConnectionError as e:
        logger.error(f"Failed to connect to OpenAI API: {e}")
        raise e
    except openai.error.RateLimitError as e:
        print(f"OpenAI API request exceeded rate limit: {e}")
        johnny.messages_to_be_deleted.append(
            johnny.bot.send_message(
                johnny.message.chat.id, templates[johnny.lang_code]["high_demand.txt"]
            )
        )
        return "[WAIT]"
    else:
        logger.info("success 🎉🎉🎉")

    logger.info(f"API completion object: {completion}")

    return completion


available_functions = {
    "google": google,
    "read_from_link": read_from_link,
}


def get_official_function_response(
    function_name: str, function_args: dict, additional_args: dict = {}
) -> list:
    """Takes function name and arguments and returns official response (dict in list)"""

    function_to_call = available_functions[function_name]
    args = {**function_args, **additional_args}
    function_response = function_to_call(**args)
    return {
        "role": "function",
        "name": function_name,
        "content": str(function_response),
    }


def load_functions_for_gpt():
    global gpt_functions_description
    with open("utils\\gpt_functions_description.json") as f:
        gpt_functions_description = json.load(f)
        return gpt_functions_description


load_functions_for_gpt()


def check_context_understanding(answer):
    """Returns bool - True if model answer assumes model understands context else False"""
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"This is text model's answer: {answer}. Is model saying it doesn't understand context? Answer Yes or No",
            }
        ],
        temperature=0,
        max_tokens=1,
    )
    logger.info(f"Check understanding completion: {completion}")
    return extract_text(completion) == "No"


def get_gpt_inline_suggestions(query):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "Generate one short suggestion. Format: '{Title}|{FewWordsDescription}|{Body}'. Answer only in this format, no additional chars, no quotes. User query: "
                + query,
            }
        ],
        temperature=1,
    )
    logger.info(
        f"Generating suggestions for inline query. Query:{query}; Suggestion:{extract_text(completion)}"
    )
    return extract_text(completion)


def check_theme_context(answer, theme):
    """Returns bool - True is answer is related to theme, False if not"""
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f'This is text mode\'l answer: "{answer}". Is model saying something about {theme}? Answer Yes or No',
            }
        ],
        temperature=0,
        max_tokens=1,
    )
    logger.info(f"Check about theme completion: {completion}")
    return extract_text(completion) == "Yes"


def improve_img_gen_prompt(start_prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"Make this prompt ({start_prompt}) for AI image generation a bit verbose and detailed",
            }
        ],
        temperature=0,
        max_tokens=40,
    )
    logger.info(
        f"Image prompt improved from {start_prompt} to {extract_text(completion)}"
    )
    return extract_text(completion)


def get_messages_in_official_format(messages):
    """Converts messages kept in Johnny to official format"""
    previous_messages = []
    for m in messages:
        if m[0] == "$FUNCTION$":
            previous_messages.append(m[1])
            continue
        previous_messages.append(
            {
                "role": ("assistant" if m[0] == "$BOT$" else "user"),
                "content": m[1],
                "name": functions.remove_utf8_chars(m[0]),
            }
        )
    return previous_messages


def speech_to_text(path):
    audio_file = open(path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript.text
