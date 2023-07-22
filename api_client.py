import requests

username = 'admin'
password = 'admin123'

url = 'http://127.0.0.1:8000/auth-jwt/token/'

response_token = requests.post(url, data={'username': username,
                                          'password': password},
                               timeout=1)

assert response_token.status_code == 200

url = 'http://127.0.0.1:8000/matches/v1.0/api/matches/'

response = requests.get(url,
                        headers={'Authorization': f'JWT {response_token.json()["access"]}'},
                        timeout=1)

assert response.status_code == 200

url = 'http://127.0.0.1:8000/matches/v1.1/api/matches/'

response = requests.get(url,
                        headers={'Authorization': f'JWT {response_token.json()["access"]}'},
                        timeout=1)

assert response.status_code == 200

if response.status_code != 200:
    refresh_url = 'http://127.0.0.1:8000/auth-jwt/token/refresh/'
    new_access = requests.post(url, response_token.json()["refresh"],
                               timeout=1,
                               ).json()["access"]
    response = requests.get(url,
                            headers={'Authorization': f'JWT {new_access}'},
                            timeout=1)
