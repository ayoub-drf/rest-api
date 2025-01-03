
import os
from django.conf import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'drf.settings'

import requests, json
from requests.auth import HTTPBasicAuth

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



from django.core.cache import cache

pages = {
    "about": "<h1>About Page</h1>",
    "contact": "<h1>Contact Page</h1>",
}

# cache.set(key="msg", value="Hello world", timeout=100) # Set to the cache

# msg_cache = cache.get("msg", default=None) # Retrieve from the cache

# cache.delete("msg") # Delete from the cache (True or False)

# Add this if msg key does not exists already in cache
# add_or_not = cache.add(key="msg", value="Hello world", timeout=100)
# print(add_or_not) # False  (already in cache)

# cache.clear()

# cache.set_many(data=pages, timeout=100, version=1)



# cache.set(key="ip_127.11.11", value=1)

# key = f"ip_127.11.11"
# request_count = cache.get(key=key, default=0)

# if request_count < 10:
#     cache.set(key="ip_127.11.11", value=request_count + 1)
#     print(request_count)


# queryset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


# page_size = 2
# page_number = 4

# start_index = queryset[(page_size * page_number) - page_size:(page_size * page_number)]

def get_formatted_response():
    url = "http://127.0.0.1:8000/books"
    headers = {
        # 'Accept': 'application/json',
        # 'Accept': 'application/xml',
        'Accept': 'application/yaml',
    }

    req = requests.get(url, headers=headers)
    print(req.text)
    print(req.status_code)


def get_exception_response():
    url = "http://127.0.0.1:8000/"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {}
    data = {
        'email': "x@aol.com"
    }
    # r = requests.get(f'{url}1', headers=headers)
    # r = requests.post(f'{url}1/', headers=headers)

    # r = requests.post(f'{url}', headers=headers)
    # r = requests.get(f'{url}', headers=headers, json=payload, auth=HTTPBasicAuth(username="x", password="x"))

    r = requests.put(f'{url}', data=data, headers=headers)



    print(r.status_code)
    print(r.json())

