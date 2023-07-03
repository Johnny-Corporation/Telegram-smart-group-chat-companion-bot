from os import environ, getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
print(load_dotenv('doc_2023-07-03_15-08-34.env'))


bot_token = environ.get("BOT_API_TOKEN")
openAI_api_key = environ.get("OPENAI_API_KEY")
developer_chat_IDs = environ.get("DEVELOPER_CHAT_IDS")

print(bot_token)