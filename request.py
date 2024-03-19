import requests

params = {
    "name": "Aleksei",
    "surname": "Kozharin",
    "age": 77,
    "registration_date": "2022-01-01"
}


resp = requests.post("http://127.0.0.1:8000/user/validate", json=params)
print(resp.json())

"""
paramm = {'name': 'AL'}

resp = requests.post("http://127.0.0.1:8000/user", params=paramm)
pprint.pprint(resp.text)

r = requests.get("/PATH/") # метод get
r_post = requests.post("/PATH/", json = {'name': 'Aleksei'}) # метод post

"""
