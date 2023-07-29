import json
from typing import List


bot_token: str

def save_admins(tgid: int):
    admins = get_admins()
    admins.append(tgid)
    js = {'bot_token': bot_token,
          'admins': admins}
    with open('config.json', 'w') as f:
        json.dump(js, f)

def get_admins() -> List[int]:
    with open('config.json', 'r') as f:
        jsconf = json.load(f)
    return jsconf['admins']


def load():
    global bot_token
    with open('config.json', 'r') as f:
        jsconf = json.load(f)
    bot_token = jsconf['bot_token']

load()