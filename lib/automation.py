from selenium import webdriver
from faker import Faker

from lib.instagram import signup
from logger import Logger
from constant import services
from httpClient import HttpClient

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
        return webdriver.Chrome('./chromedriver')

    async def generate_instagram_account(self, profile_id):
        CountryId = '15'
        user = {'username': fake.internet.user_name(), 'password': fake.internet.password(),
                'firstName': fake.person.first_name(), 'lastName': fake.person.last_name()}

        user.username = user['username'].strip().lower().replace(
            '[^\d\w-]', '-').replace('_', '-') \
            .replace('^-', '').replace('-$', '') \
            .replace('--', '-').replace('-', '')

        SmSPoolAPI = 'https://api.smspool.net/purchase/sms'
        key = 'hFXGJFunoIckg01PLNJlEqHG5IcG8niv'

        for element in service_list.get_services():
            if element['name'] == 'United Kingdom':
                CountryId = element['ID']

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

        browser = await self.browser_local(profile_id)
        await signup(browser, user, profile_id)
