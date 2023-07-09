import os

import configparser

from selenium import webdriver
from faker import Faker
from lib.crawler import start_crawler
from lib.instagram.instagramSignup import signup
from lib.instagram.likePosts import like_post_run_program, like_post
from lib.instagram.signin import signin, update_profile_bio
from lib.instagram.uploadProfilePhoto import upload_profile_photo, upload_media_photo
from lib.instagram.followAccounts import follow_accounts
from lib.pexel_api import download_random_image
from logger import Logger
from constant import services
from httpClient import HttpClient

import chromedriver_autoinstaller

fake = Faker()
service_list = services.ServiceList()
logger = Logger.get_instance()


async def browser_local():
    logger.info("browser_local")
    # chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
    return webdriver.Chrome('./chromedriver/chromedriver')


# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Determine the environment from the command-line argument
input_environment = os.environ.get('ENVIRONMENT', 'Local')

env = config[input_environment]


async def browser_multilogin(profile_id):
    json_response = await HttpClient("http://127.0.0.1:35000/api/v1/profile") \
        .get(f"/start?automation=true&profileId={profile_id}")
    return webdriver.Remote(command_executor=json_response['value'])


class Automation:
    def __init__(self, profile_id):
        logger.info("Automation instance")
        self.profile_id = profile_id
        self.environment = env

    async def sign_in_to_instagram(self, user):
        logger.info("sign_in_to_instagram")
        browser = await self.get_browser()
        await signin(browser, user)
        return browser

    async def instagram_like_posts(self, user, daily_limit):
        browser = await self.sign_in_to_instagram(user)
        await like_post(browser, daily_limit)
        browser.quit()

    async def instagram_upload_profile_photo(self, user, photo_path):
        browser = await self.sign_in_to_instagram(user)
        await upload_profile_photo(browser, photo_path)
        browser.quit()

    async def instagram_update_bio(self, user):
        browser = await self.sign_in_to_instagram(user)
        logger.info("Signin browser found")
        quote = fake.sentence(nb_words=10, variable_nb_words=True)
        await update_profile_bio(browser, user, quote)
        browser.quit()

    async def instagram_follow_accounts(self, user, follow_count):
        browser = await self.sign_in_to_instagram(user)
        logger.info("Signin browser found")
        await follow_accounts(browser, follow_count)
        browser.quit()

    async def generate_instagram_account(self):
        CountryId = '15'
        profile = fake.simple_profile()
        user = {'username': profile['username'], 'password': fake.password(length=12),
                'name': profile['name']}

        for element in service_list.get_services():
            if element.name == 'United States':
                CountryId = element.id

        ServiceId = '457'
        jsonData = await HttpClient(self.environment['sms_pool_purchase_api']) \
            .get(f"?key={self.environment['key']}&country={CountryId}&service={ServiceId}")
        phoneNumber = jsonData['phonenumber']
        orderId = jsonData['order_id']
        country = jsonData['country']
        success = jsonData['success']
        countryCode = jsonData['cc']
        message = jsonData['message']

        user['number'] = str(phoneNumber)
        user['orderId'] = orderId
        user['key'] = self.environment['key']

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

        browser = await self.get_browser()

        await signup(self.environment, browser, user, self.profile_id)

    async def get_browser(self):
        browser = await browser_multilogin(self.profile_id) \
            if self.environment.getboolean('isProd') \
            else await browser_local()
        return browser

    async def create_browser_history(self):
        browser = await self.get_browser()
        await start_crawler(browser, self.profile_id)

    async def instagram_upload_media_photo(self, user):
        browser = await self.sign_in_to_instagram(user)
        # media_path, caption = await download_random_image()
        # await upload_media_photo(browser, media_path, caption)
        # browser.quit()
        await follow_accounts(browser, 30)
