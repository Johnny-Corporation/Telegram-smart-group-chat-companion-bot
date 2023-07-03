import os
import openai


from dotenv import load_dotenv
from os import environ, getenv

load_dotenv(".env")
bot_token = environ.get("BOT_API_TOKEN")
openAI_api_key = environ.get("OPENAI_API_KEY")
developer_chat_IDs = environ.get("DEVELOPER_CHAT_IDS")

openai.organization = environ.get("OPENAI_ORGANIZATION")
openai.api_key = openAI_api_key
model = "gpt-3.5-turbo"               #------------------------------------------
#print(openai.Model.list())

def question_to_bot(message):
    message_to_gpt = ''

    for i in range(message.index(' ')+1, len(message)):
        message_to_gpt = message_to_gpt + message[i]

    model = "gpt-3.5-turbo" #!!!!!!!!!!!!!!!!!!!!!!!!!1Can be changed (connect with more global)!!!!!!!!!!!!!!!!!
    system_content = 'Answer the question' #!!!!!!!!!!!!!!!!!!!!!Can be changed!!!!!!!!!!!!!!!!!!!!!!!!!!

    return get_response(message_to_ai(model,system_content,message_to_gpt))
    
    
    








def message_to_ai(model, system_content, user_content):
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
    )

    return completion

def get_tokens(completion):
    tokens_total = completion.usage.total_tokens

    #print(f"Tokens: {tokens_total}")

    return tokens_total

def get_response(completion):

    #print(f"Message: {message_back}")

    return completion.choices[0].message.content

