import requests
import json
import uuid
from os import environ


def get_access_token():
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        "Authorization": f"Basic {environ['sber_auth_request_token']}",
        "RqUID": str(uuid.uuid4()),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"scope": "SALUTE_SPEECH_PERS"}

    response = requests.post(url, headers=headers, data=data, verify=False)

    if response.status_code == 200:
        token_data = json.loads(response.text)
        return token_data["access_token"]  # , token_data["expires_at"]
    else:
        (f"Error: {response.status_code}, {response.text}")
        return None, None
