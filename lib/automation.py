from selenium import webdriver
from faker import Faker

from lib.crawler import start_crawler
from lib.instagram.instagramSignup import signup
from lib.instagram.signin import signin
from logger import Logger
from constant import services
from httpClient import HttpClient

import chromedriver_autoinstaller

fake = Faker()
service_list = services.ServiceList()
logger = Logger.get_instance()


class Automation:
    def __init__(self, profile_id):
        self.profile_id = profile_id

    async def browser_multilogin(self, profile_id):
        json_response = await HttpClient("http://127.0.0.1:35000/api/v1/profile") \
            .get(f"/start?automation=true&profileId={profile_id}")
        return webdriver.Remote(command_executor=json_response['value'])

    async def browser_local(self, profile_id):
        # chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
        return webdriver.Chrome('./chromedriver/chromedriver')


    async def instagram_sign_in(self):
        browser = await self.browser_local(self.profile_id)
        await signin(browser)

    async def generate_instagram_account(self, environment):
        CountryId = '15'
        profile = fake.simple_profile()
        user = {'username': profile['username'], 'password': fake.password(length=12),
                'name': profile['name']}

        for element in service_list.get_services():
            if element.name == 'United States':
                CountryId = element.id

        ServiceId = '457'
        jsonData = await HttpClient(environment['sms_pool_purchase_api']) \
            .get(f"?key={environment['key']}&country={CountryId}&service={ServiceId}")
        phoneNumber = jsonData['phonenumber']
        orderId = jsonData['order_id']
        country = jsonData['country']
        success = jsonData['success']
        countryCode = jsonData['cc']
        message = jsonData['message']

        user['number'] = str(phoneNumber)
        user['orderId'] = orderId
        user['key'] = environment['key']

        print('[UserInformation]', {
            'phoneNumber': user['number'],
            'orderId': orderId,
            'country': country,
            'success': success,
            'countryCode': countryCode,
            'message': message
        })

        if message.startswith('This country is currently not available for this service'):
            print('[Error Message]', {'jsonData': jsonData})

        browser = await self.get_browser(environment)

        await signup(environment, browser, user, self.profile_id)

    async def get_browser(self, environment):
        browser = await self.browser_multilogin(self.profile_id) \
            if environment.getboolean('isProd') \
            else await self.browser_local(self.profile_id)
        return browser

    async def create_browser_history(self,environment):
        browser = await self.get_browser(environment)
        await start_crawler(browser)