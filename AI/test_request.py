import requests
import json

payload = {
    "message": "Помоги с классификацией Titanic",
    "context": []
}

response = requests.post("address",
                         headers={"AI_BACKEND_KEY": "Something"},
                         data={"payload": json.dumps(payload)})
print(response.json())