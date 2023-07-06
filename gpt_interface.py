import openai
from os import environ

openAI_api_key = environ.get("OPENAI_API_KEY")
if not openAI_api_key:
    print("Failed to load OpenAI API key from environment, exiting...")
    exit()
openai.api_key = openAI_api_key


def check_negative_answer(text: str) -> bool:
    """Checks wether input text is negative answer or not"""
    pass


def chat_message(context: list) -> str:
    pass
