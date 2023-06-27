import asyncio
import os

from aioconsole import ainput

from httpClient import HttpClient
from lib.automation import Automation
from logger import Logger

import configparser

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')
logger = Logger.get_instance()

# Determine the environment from the command-line argument
input_environment = os.environ.get('ENVIRONMENT', 'Local')

env = config[input_environment]


async def main():
    actions = {
        '1': create_multilogin_profile,
        '2': create_instagram_account,
        '3': sign_in_instagram_account,
        '4': exit_program,
        '5': crawl
    }

    while True:
        print('=========\n' +
              'Enter action to perform.\n' +
              '1. Create Multilogin Profile\n' +
              '2. Create Instagram Account\n' +
              '3. SignIn Instagram Account\n' +
              '4. Exit\n' +
              '5. Crawl\n' +
              '=========\n')

        user_input = await ainput("Please enter your input: ")

        # Perform actions based on user input
        action = actions.get(user_input)
        if action:
            await action()
        else:
            # Handle invalid input
            print("Invalid input. Please try again.\n")


async def create_multilogin_profile():
    profile_count = await ainput("Input number of profiles to be created: ")
    jsonData = await HttpClient("http://localhost:3001").post(f"/profile/generate/{profile_count}")
    logger.info(jsonData)
    # Your code for creating a Multilogin profile goes here


async def create_instagram_account():
    print("Creating Instagram Account...")
    jsonData = await HttpClient("http://localhost:3001").get("/profile/unused")
    for profile in jsonData['profiles']:
        logger.info(profile['uuid'])
        bot = Automation(profile['uuid'])
        await bot.generate_instagram_account(env)


async def sign_in_instagram_account():
    bot = Automation('dummyUUid')
    await bot.instagram_sign_in()


def exit_program():
    print("Exiting...")
    raise SystemExit


async def crawl():
    jsonData = await HttpClient("http://localhost:3001").get("/profile/unused")
    for profile in jsonData['profiles']:
        logger.info(profile['uuid'])
        bot = Automation(profile['uuid'])
        await bot.create_browser_history(env)


asyncio.run(main())
