#!/bin/python
import requests
from mastodon import Mastodon
### ------------------------------------------------------------------------------- ###
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

NOTIFYTYPE="admin.report"

SIGNALHOST=config["Signal"]["SIGNALHOST"]
PHONENUMBER=config["Signal"]["PHONENUMBER"]
SIGNALRECIPIENTIDLIST=config["Signal"]["SIGNALRECIPIENTIDLIST"]
SIGNALRECIPIENTIDLIST = SIGNALRECIPIENTIDLIST.strip("[]").split(",")

access_token_a=config["Mastodon"]["TOKEN"]
api_base_url_a=config["Mastodon"]["API_URL"]
### ------------------------------------------------------------------------------- ###
def SendMessage(Message: str) -> None:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
### ------------------------------------------------------------------------------- ###
    for contact in SIGNALRECIPIENTIDLIST:
        json_data = {
            'message': f'{Message}',
            'number': f'{PHONENUMBER}',
            'recipients': [f"{contact}",]
        }
        response = requests.post(f"{SIGNALHOST}/v2/send", headers=headers, json=json_data)
### ------------------------------------------------------------------------------- ###
### ------------------------------------------------------------------------------- ###
    if response.status_code != 201:
        print(f"\
The API has returned an error.\n\
The response code is: {response.status_code}\n\
The message given is: {response.text}"
        )
        raise RuntimeError
### ------------------------------------------------------------------------------- ###
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
    print(f'Der {USER} wurde wegen angeblicher "{GRUND}" am {str(DATUM)[:19]} von {MELDER} gemeldet {LINKZUMREPORT}')
### ------------------------------------------------------------------------------- ###
    SendMessage(f'Der {USER} wurde wegen angeblicher "{GRUND}" am {str(DATUM)[:19]} von {MELDER} gemeldet {LINKZUMREPORT}')
### ------------------------------------------------------------------------------- ###

E = "E"

#Obst=[{"name": "Bananen", "preis": 1.50}, {"name": "Apfel", "preis": 23.60}, {"name": "Pfirsich", "preis": 2}]
#
#for obs in Obst:
#    print(f"Der {obs['name']} kostet {obs['preis']}€")
