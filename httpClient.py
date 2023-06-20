import requests


class HttpClient:
    def __init__(self, base_url, logger):
        self.base_url = base_url
        self.logger = logger

    def get(self, path, params=None, headers=None):
        url = self.base_url + path
        self.logger.info(f"GET {url}")
        response = requests.get(url, params=params, headers=headers)
        self.logger.info(f"Response Status Code: {response.status_code}")
        return response

    def post(self, path, data=None, headers=None):
        url = self.base_url + path
        self.logger.info(f"POST {url}")
        response = requests.post(url, json=data, headers=headers)
        self.logger.info(f"Response Status Code: {response.status_code}")
        return response

    def delete(self, path, headers=None):
        url = self.base_url + path
        self.logger.info(f"DELETE {url}")
        response = requests.delete(url, headers=headers)
        self.logger.info(f"Response Status Code: {response.status_code}")
        return response

    def put(self, path, data=None, headers=None):
        url = self.base_url + path
        self.logger.info(f"PUT {url}")
        response = requests.put(url, json=data, headers=headers)
        self.logger.info(f"Response Status Code: {response.status_code}")
        return response
