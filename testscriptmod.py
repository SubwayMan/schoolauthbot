import requests
from requests.structures import CaseInsensitiveDict

url = "https://outlook.office.com/search/api/v1/suggestions?scenario=owa.react.compose&setflight=CSRClientEnabled&n=133&cri=6c18963c-4ab2-b0dc-760a-62f93017d451&cv=E%2FRjcmQ9tI58XtBG5E9C33.133"

headers = CaseInsensitiveDict()
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"
headers["Accept"] = "*/*"
headers["Accept-Language"] = "en-CA,en-US;q=0.7,en;q=0.3"
headers["Content-Type"] = "application/json"
headers["client-request-id"] = "placeholder"
headers["client-session-id"] = "placeholder"
headers["ms-cv"] = "placeholder"
headers["x-anchormailbox"] = "placeholder"
headers["x-ms-appname"] = "owa-reactmail"
headers["x-owa-canary"] = "placeholder"
headers["x-owa-sessionid"] = "placeholder"
headers["Origin"] = "https://outlook.office.com"
headers["Sec-Fetch-Dest"] = "empty"
headers["Sec-Fetch-Mode"] = "cors"
headers["Sec-Fetch-Site"] = "same-origin"
headers["authorization"] = "Bearer  bearerhere"
headers["Connection"] = "keep-alive"
headers["TE"] = "trailers"

query = input("enter query ")
data = '{"AppName":"OWA","Scenario":{"Name":"owa.react.compose"},"Cvid":"placeholder","EntityRequests":[{"Query":{"QueryString":"' + query + '"},"EntityType":"People","Provenances":["Mailbox","Directory"],"Size":"20","Fields":["Id","ADObjectId","DisplayName","EmailAddresses","PeopleSubtype","PeopleType","PDLItemId","PersonaId","ImAddress","JobTitle","FeatureData","PersonId"]}]}'


resp = requests.post(url, headers=headers, data=data)

c = open("scriptoutput.json", "w")
c.write(resp.text)
c.close()

