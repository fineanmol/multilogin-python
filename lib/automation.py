from selenium import webdriver
from faker import Faker

from lib.instagram import signup
from logger import Logger
from constant import services
from httpClient import HttpClient

import chromedriver_autoinstaller

fake = Faker()
service_list = services.ServiceList()
logger = Logger()


class Automation:
    def __init__(self, profile_id):
        self.profile_id = profile_id

    async def browser_multilogin(self, profile_id):
        json_response = await HttpClient("http://127.0.0.1:35000/api/v1/profile", logger) \
            .get(f"/start?automation=true&profileId={profile_id}")
        return webdriver.Remote(command_executor=json_response['value'])

    async def browser_local(self, profile_id):
        chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
        return webdriver.Chrome()

    async def generate_instagram_account(self):
        CountryId = '15'
        profile = fake.simple_profile()
        user = {'username': profile['username'], 'password': fake.password(length=12),
                'name': profile['name']}

        # user.username = user['username'].strip().lower().replace(
        #     '[^\d\w-]', '-').replace('_', '-') \
        #     .replace('^-', '').replace('-$', '') \
        #     .replace('--', '-').replace('-', '')

        SmSPoolAPI = 'https://api.smspool.net/purchase/sms'
        key = 'hFXGJFunoIckg01PLNJlEqHG5IcG8niv'

        for element in service_list.get_services():
            if element.name == 'United States':
                CountryId = element.id

        ServiceId = '457'
        jsonData = await HttpClient(SmSPoolAPI, logger).get(f"?key={key}&country={CountryId}&service={ServiceId}")
        phoneNumber = jsonData['phonenumber']
        orderId = jsonData['order_id']
        country = jsonData['country']
        success = jsonData['success']
        countryCode = jsonData['cc']
        message = jsonData['message']

        user['number'] = '+' + str(countryCode) + str(phoneNumber)
        user['orderId'] = orderId
        user['key'] = key

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

        browser = await self.browser_local(self.profile_id)
        await signup(browser, user, self.profile_id)