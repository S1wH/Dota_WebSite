import base64
import requests

# url = "http://127.0.0.1:8000/matches/api/matches/"
#
# response = requests.get(url, timeout=1)
# assert response.status_code == 401
#
# login = 'admin'
# password = 'admin123'
# auth_data = f'{login}:{password}'
#
# sample_string_bytes = auth_data.encode("ascii")
#
# base64_bytes = base64.b64encode(sample_string_bytes)
# base64_string = base64_bytes.decode("ascii")
#
# headers = {
#     'Authorization': f'Basic {base64_string}'
# }
#
#
# response = requests.get(url, headers=headers, timeout=1)
# assert response.status_code == 200, response.status_code
#
# token = '7013ec96a0c3db91010a57657f223b6334080a6f'
#
# headers = {
#     'Authorization': f'Token {token}'
# }
#
#
# response = requests.get(url, headers=headers, timeout=1)
# assert response.status_code == 200, response.status_code
#
# # get token
#
# url = 'http://127.0.0.1:8000/api-token-auth/'
#
# response = requests.post(url, data={'username': 'admin', 'password': 'admin123'}, timeout=1)
#
# token = response.json()['token']
#
# headers = {
#     'Authorization': f'Token {token}'
# }
#
# url = "http://127.0.0.1:8000/matches/api/matches/"
# response = requests.get(url, headers=headers, timeout=1)
# assert response.status_code == 200, response.status_code

# url = 'http://127.0.0.1:8000/auth/users/'

username = 'admin'
password = 'admin123'

url = 'http://127.0.0.1:8000/auth-jwt/token/'

response_token = requests.post(url, data={'username': username,
                                          'password': password},
                               timeout=1)

assert response_token.status_code == 200

url = 'http://127.0.0.1:8000/matches/api/matches/'

response = requests.get(url, headers={'Authorization': f'JWT {response_token.json()["access"]}'})

assert response.status_code == 200

if response.status_code != 200:
    refresh_url = 'http://127.0.0.1:8000/auth-jwt/token/refresh/'
    new_access = requests.post(url, response_token.json()["refresh"]).json()["access"]
    response = requests.get(url,
                            headers={'Authorization': f'JWT {new_access}'})
