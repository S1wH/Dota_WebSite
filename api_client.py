import requests
import base64


url = "http://127.0.0.1:8000/matches/api/matches/"

response = requests.get(url)
assert response.status_code == 401

login = 'admin'
password = 'admin123'
auth_data = f'{login}:{password}'

sample_string_bytes = auth_data.encode("ascii")

base64_bytes = base64.b64encode(sample_string_bytes)
base64_string = base64_bytes.decode("ascii")

headers = {
    'Authorization': f'Basic {base64_string}'
}


response = requests.get(url, headers=headers)
assert response.status_code == 200, response.status_code

token = '7013ec96a0c3db91010a57657f223b6334080a6f'

headers = {
    'Authorization': f'Token {token}'
}


response = requests.get(url, headers=headers)
assert response.status_code == 200, response.status_code

# get token

url = 'http://127.0.0.1:8000/api-token-auth/'

response = requests.post(url, data={'username': 'admin', 'password': 'admin123'})

token = response.json()['token']

headers = {
    'Authorization': f'Token {token}'
}

url = "http://127.0.0.1:8000/matches/api/matches/"
response = requests.get(url, headers=headers)
assert response.status_code == 200, response.status_code
