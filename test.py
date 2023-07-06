import gpt_functions as gpt
import openai

gpt_token = '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'
organization_token = 'org-pQuAcA9nvf69dTMuXLO1cRNo'

model = "gpt-3.5-turbo" #!!!!!!!!!!!!!!!!!!!!!!!!!1Can be changed (connect with more global)!!!!!!!!!!!!!!!!!
system_content = 'Read the previous messages and write something useful' #!!!!!!!!!!!!!!!!!!!!!Can be changed!!!!!!!!!!!!!!!!!!!!!!!!!!

openai.api_key = str(gpt_token)
openai.organization = organization_token


completion = openai.ChatCompletion.create(
    model=model,
    messages=[
        {"role": "system", "content": system_content},
        {"role": "user", "content": 'User1: What about stocks?'},
        {"role": "user", "content": 'I think that is a origin of good pay,'},
        {"role": "user", "content": 'Are there something?'}
    ]
)


print(gpt.get_response(completion))