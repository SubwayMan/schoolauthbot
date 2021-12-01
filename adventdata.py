import requests
from requests.structures import CaseInsensitiveDict
import json
from dotenv import load_dotenv
import os

load_dotenv()

def get_advent_data(event="2021") -> dict:
    url = "https://adventofcode.com/" + event + "/leaderboard/private/view/726706.json"

    headers = CaseInsensitiveDict()
    headers["cookie"] = os.environ.get("adventcookie")
    resp = requests.get(url, headers=headers)

    dat = json.loads(resp.text)
    return dat



