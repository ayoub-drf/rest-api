
import os
from django.conf import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'drf.settings'

import requests, json

url, token, refresh, notes = "http://127.0.0.1:8000/", "token/", "token/refresh/", "notes/"

def getToken():
    user = {"username": "x", "password": "x"}
    r = requests.post(f"{url}{token}", json=user)
    with open('x.json', 'w') as f:
        json.dump(r.json(), f, indent=4)

def getNotes():
    headers = {"Content-Type": "application/json"}
    with open('x.json', 'r') as f:
        data = json.load(f)
        headers["Authorization"] = f"Bearer {data['access']}"

        r = requests.get(f"{url}{notes}", headers=headers)
        if r.status_code == 200:
            print(r.json())
        
        if r.status_code == 401:
            print('The access token expired')


        if r.status_code == 401:
            print("Send a post request to 'token/refresh/'")
            refreshToken = {'refresh': data['refresh']}
            r = requests.post(f"{url}{refresh}", json=refreshToken)

            if r.status_code == 401:
                print('The refresh token expired')

def checkCache():
    mobile = "Mozilla/5.0 (Linux; Android 15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.81 Mobile Safari/537.36"
    pc = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.2903.51'

    headers = {
        "Content-Type": "application/json",
        "User-Agent": mobile
    }

    r = requests.get('http://127.0.0.1:8000/', headers=headers)

    print(r.json())






