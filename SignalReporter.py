#!/bin/python
import requests
from mastodon import Mastodon

HOST="http://10.100.100.211:8080"
PHONENUMBER=""
SIGNALGROUPID=""
NOTIFYTYPE="admin.report"
# Falls moeglich, niemals credentials im Code unterbringen. Das geht schnell versehentlich ins github committet. Config-Datei oder Environment-Variable wäre gut
#TODO: Create SECRETS.env
#TODO: Revoke access token
#TODO: Create dedicated user on mastodon
access_token_a='UtKw8-7G0mR6IAvHOEE9JRTJq1i5gC7mYPxrGJyqEsU'
api_base_url_a='https://mastodon.de'

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
    print(response.content)

mastodon = Mastodon(
    access_token= access_token_a,
    api_base_url= api_base_url_a
)

notifs = mastodon.notifications()
reports = []


for noty in notifs:
    if noty["type"] == NOTIFYTYPE:
        reports.append(noty)

for report in reports:
    USER          = report["report"]["target_account"]["acct"]
    GRUND         = report["report"]["comment"]
    DATUM         = report["report"]["created_at"]
    MELDER        = report["account"]["acct"]
    LINKZUMREPORT = f"{api_base_url_a}/admin/reports/{report['report']['id']}"
    print("\n")
    print(f"Der {USER} wurde wegen {GRUND} am {str(DATUM)[:19]} von {MELDER} gemeldet {LINKZUMREPORT}")

E = "E"

#print(reports)


#Obst=[{"name": "Bananen", "preis": 1.50}, {"name": "Apfel", "preis": 23.60}, {"name": "Pfirsich", "preis": 2}]
#
#for obs in Obst:
#    print(f"Der {obs['name']} kostet {obs['preis']}€")
