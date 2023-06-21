import aiohttp


class HttpClient:
    def __init__(self, base_url, logger):
        self.base_url = base_url
        self.logger = logger

    async def get(self, path, params=None, headers=None):
        url = self.base_url + path
        self.logger.info(f"GET {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                self.logger.info(f"Response Status Code: {response.status}")
                return await response.json()

    async def post(self, path, data=None, headers=None):
        url = self.base_url + path
        self.logger.info(f"POST {url}")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                self.logger.info(f"Response Status Code: {response.status}")
                return await response.json()

    async def delete(self, path, headers=None):
        url = self.base_url + path
        self.logger.info(f"DELETE {url}")
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers) as response:
                self.logger.info(f"Response Status Code: {response.status}")
                return await response.json()

    async def put(self, path, data=None, headers=None):
        url = self.base_url + path
        self.logger.info(f"PUT {url}")
        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=data, headers=headers) as response:
                self.logger.info(f"Response Status Code: {response.status}")
                return await response.json()
