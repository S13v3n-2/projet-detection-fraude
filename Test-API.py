import requests

url = "http://127.0.0.1:8000/predict/xgboost"

headers = {
    "Content-Type": "application/json"
}

data = {
    "amt": 240000.84,
    "zip": 79759,
    "city_pop": 23,
    "age_at_transaction": 50,
    "unix_time": 1371852399,
    "state": "TX",
    "city": "Notrees",
    "gender": "F",
    "category": "health_fitness",
    "merchant": "fraud_Hamill-D'Amore",
    "job": "Cytogeneticist"
}

response = requests.post(
    url,
    json=data,
    headers=headers
)

print(response.status_code)
print(response.json())
