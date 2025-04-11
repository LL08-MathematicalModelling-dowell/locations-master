
import requests
import json

url = "https://datacube.uxlivinglab.online/api/add_collection/"
fields = [{'name': 'hour', 'type':'number'},]
for i in range(1, 3601):
    d = {}
    d['name'] = str(i)
    d["type"] = 'string'
    fields.append(d)

payload = json.dumps({
  "database_id": "67cac9e93fb4f7ad9ac6c30e",
  "collections": [
    {
      "name": "process_v2",
      "fields": fields
    }
  ]
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

