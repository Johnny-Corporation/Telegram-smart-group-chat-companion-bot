import os
import openai


from dotenv import load_dotenv
from os import environ, getenv

load_dotenv(".env")
bot_token = environ.get("BOT_API_TOKEN")
openAI_api_key = environ.get("OPENAI_API_KEY1")
developer_chat_IDs = environ.get("DEVELOPER_CHAT_IDS")

openai_organization = environ.get("OPENAI_ORGANIZATION")
model = "gpt-3.5-turbo"               #------------------------------------------
#print(openai.Model.list())


openai.api_key =  openAI_api_key
openai.organization = openai_organization

completion = openai.ChatCompletion.create(
    model=model,
    messages=[
        {"role": "system", "content": 'write short answer'},
        {"role": "user", "content": 'User 1: let"s walk tomorrow. User 2: When?'},
    ]
)

print(completion.choices[0].message.content)
