import aiohttp

BASE_URL = 'http://127.0.0.1:8000/'


async def get_token():
    url = BASE_URL + 'auth-jwt/token/'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data={
            'username': 'admin',
            'password': 'admin123',
        }) as response:
            return await response.json()


async def refresh_token(token):
    url = BASE_URL + 'auth-jwt/token/refresh/'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data={"Refresh": token["refresh"]}) as response:
            return await response.json()


async def set_connection(url: str, token):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=
        {'Authorization': f'JWT {token["access"]}'}) as response:
            response = await response.json()
            if await check_authorization(response):
                return response
            return 'NO'


async def check_authorization(response: dict):
    if 'results' in response.keys():
        return True
    return False


async def make_request(url: str, token):
    response = await set_connection(url, token)
    if response == 'NO':
        return None
    return response['results']
