
import openai
import pandas as pd

OPENAI_API_KEY1='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'
OPENAI_ORGANIZATION='org-pQuAcA9nvf69dTMuXLO1cRNo'

openai.api_key = OPENAI_API_KEY1
openai.organization = OPENAI_ORGANIZATION
model = "gpt-3.5-turbo"

temporary_memory = ['/start', ["print a letter 'A'",'A']]

patterns = [{"role": "system", "content": 'give  short answer'},{"role": "user", "content": "print a letter 'A'"}]

# completion1 = openai.ChatCompletion.create(
#     model=model,
#     messages=[
#         pattern1,
#         pattern2,
#         {"role": "assistant", "content": "A"},
#         {"role": "user", "content": "write the next letter"}
#     ]
# )
# print(completion1)

completion2 = openai.ChatCompletion.create(
    model=model,
    messages=patterns
)

print('')
print(completion2)