import requests
from requests.structures import CaseInsensitiveDict
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://outlook.office.com/search/api/v1/suggestions?scenario=owa.react.compose&setflight=CSRClientEnabled&n=95&cri=0f9e6e2f-435b-d7c2-9527-dec4412c49e3&cv=mkpDCKnmGlOOQ7XkWwY2Vs.95"

class BadInputError():
    """Custom error."""
    pass

class UserNotFoundError():
    """Custom Error."""
    pass

headers = CaseInsensitiveDict()
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"
headers["Accept"] = "*/*"
headers["Accept-Language"] = "en-CA,en-US;q=0.7,en;q=0.3"
headers["Content-Type"] = "application/json"
headers["client-request-id"] = os.environ.get("xhr-request-id")
headers["client-session-id"] = os.environ.get("xhr-session-id")
headers["ms-cv"] = os.environ.get("xhr-ms-cv")
headers["x-anchormailbox"] = os.environ.get("xhr-ms-cv")
headers["x-ms-appname"] = "owa-reactmail"
headers["x-owa-canary"] = os.environ.get("x-owa-canary")
headers["x-owa-sessionid"] = os.environ.get("x-owa-sessionid")
headers["Origin"] = "https://outlook.office.com"
headers["Sec-Fetch-Dest"] = "empty"
headers["Sec-Fetch-Mode"] = "cors"
headers["Sec-Fetch-Site"] = "same-origin"
headers["authorization"] = os.environ.get("xhr-auth")
headers["Connection"] = "keep-alive"
headers["Pragma"] = "no-cache"
headers["Cache-Control"] = "no-cache"
headers["TE"] = "trailers"

def send_req(txt):
    if not txt.isalnum():
        return 1

    data = '{"AppName":"OWA","Scenario":{"Name":"owa.react.compose"},"Cvid":"' + \
        os.environ.get("cvid") + '","EntityRequests":[{"Query":{"QueryString":"' + \
        txt + \
        '"},"EntityType":"People","Provenances":["Mailbox","Directory"],"Size":"20","Fields":["Id","ADObjectId","DisplayName","EmailAddresses","PeopleSubtype","PeopleType","PDLItemId","PersonaId","ImAddress","JobTitle","FeatureData","PersonId"]}]}'

    resp = requests.post(url, headers=headers, data=data)
    print(resp.text)
    respjson = json.loads(resp.text)
    if not respjson["Groups"] or len(respjson["Groups"][0]["Suggestions"]) != 1:
        return 1
    
    return respjson["Groups"][0]["Suggestions"][0]

