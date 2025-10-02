import requests

url = "http://localhost:8000/predict"
headers = {"Content-Type": "application/json"}
payload = {
    "data": [
        {
            "id": 1,
            "text": "пример запроса"
        }
    ]
}

response = requests.post(url, headers=headers, json=payload)

print("Status code:", response.status_code)
print("Response:", response.json())
