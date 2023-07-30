import openai
from os import environ
from utils.logger import logger  # needed for hidden logs, do not remove
import utils.functions as functions

openAI_api_key = environ.get("OPENAI_API_KEY")
if not openAI_api_key:
    print("Failed to load OpenAI API key from environment, exiting...")
    exit()
openai.api_key = openAI_api_key


def extract_tokens(completion: openai.ChatCompletion) -> int:
    """Extracts tokens from OpenAI API response"""
    return [completion.usage.prompt_tokens, completion.usage.completion_tokens]


def extract_text(completion: openai.ChatCompletion) -> str:
    """Extracts text from OpenAI API response"""
    return completion.choices[0].message.content


def create_chat_completion(
    messages: list,
    lang: str = 'en',
    system_content: str = None,
    answer_length: int = "as you need",
    reply: bool = False,  # SYS
    model: str = "gpt-3.5-turbo",
    temperature: int = 1,
    top_p: float = 0.5,
    n: int = 1,
    stream: bool = False,
    stop: str = None,
    frequency_penalty: float = 0,
    presense_penalty: float = 0,
) -> openai.ChatCompletion:
    """Creates ChatCompletion
    messages(list): list of dicts, where key is users name and value is his message
    reply(bool): True means GPT will consider last message, False means not, None means system input field will be empty
    """

    system_content = "You are a group chat participant. "
    if reply:
        system_content += "Focus on the last message. "

    system_content += "Ask questions if you need. "
    system_content += f"Your answer should be {answer_length}. "

    previous_messages = [
        {
            "role": "system",
            "content": functions.translate_text(lang,system_content),
        }
    ]

    for m in messages:
        previous_messages.append(
            {
                "role": ("assistant" if m[0] == "assistant" else "user"),
                "content": m[1],
                "name": functions.remove_utf8_chars(m[0]),
            }
        )

    completion = openai.ChatCompletion.create(
        model=model,
        messages=previous_messages,
        temperature=temperature,
        top_p=top_p,
        n=n,
        stream=stream,
        stop=stop,
        frequency_penalty=frequency_penalty,
        presence_penalty=presense_penalty,
    )

    return completion


def check_context_understanding(answer):
    """Returns bool - True if model answer assumes model understands context else False"""
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"This is text model's answer: {answer}. Is model saying it doesn't understand context and/or just trying to keep up conversation? Answer Yes or No",
            }
        ],
        temperature=0,
        max_tokens=1,
    )
    return extract_text(completion) == "No"


def check_theme_context(answer, theme):
    """Returns bool - True is answer is related to theme, False if not"""
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"This is text model's answer: {answer}. Is model saying something about {theme}? Answer Yes or No",
            }
        ],
        temperature=0,
        max_tokens=1,
    )
    return extract_text(completion) == "Yes"


def get_messages_in_official_format(messages):
    """Converts messages kept in Johnny to official format"""
    previous_messages = []
    for m in messages:
        previous_messages.append(
            {
                "role": ("assistant" if m[0] == "assistant" else "user"),
                "content": m[1],
                "name": functions.remove_utf8_chars(m[0]),
            }
        )
    return previous_messages


def speech_to_text(path):
    audio_file= open(path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript.text
