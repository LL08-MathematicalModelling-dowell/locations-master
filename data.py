import requests
hour = '1'

url = 'https://datacube.uxlivinglab.online/api/crud?database_id=67cac9e93fb4f7ad9ac6c30e&collection_name=process_v2&filter={"hour":1}&limit=0&offset=0'

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)




print(response.text)





#import requests
#import json
#
#url = "https://datacube.uxlivinglab.online/api/crud/"
#hour_dict = {}
#
#hour_dict["hour"] = 1
#for i in range(1, 3601):
#    hour_dict[str(i)] = None
#
#payload = json.dumps({
#  "database_id": "67cac9e93fb4f7ad9ac6c30e",
#  "collection_name": "process_v2",
#  "data": [ hour_dict ]
#})
#headers = {
#  'Content-Type': 'application/json'
#}
#
#response = requests.request("POST", url, headers=headers, data=payload)
#
#print(response.text)
#
