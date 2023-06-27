import requests

url = 'http://127.0.0.1:8000/api/'

response = requests.get(url, timeout=1)

print(response.status_code)

print(response.json())


response = requests.options(url, timeout=1)

print(response.status_code)

print(response.json())

url = 'http://127.0.0.1:8000/api/users/1/'

response = requests.patch(url, data={'is_staff': False}, timeout=1)

print(response.status_code)

print(response.json())

response = requests.get(url, timeout=1)

print(response.status_code)

print(response.json())
