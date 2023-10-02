#!/bin/python
import requests

HOST="http://10.100.100.211:8080"
PHONENUMBER=""
SIGNALGROUPID=""

def SendMessage(Message: str) -> None:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    json_data = {
        'message': f'{Message}',
        'number': f'{PHONENUMBER}',
        'recipients': [
            f'{SIGNALGROUPID}',
        ]
    }
    response = requests.post(f"{HOST}/v2/send", headers=headers, json=json_data)

