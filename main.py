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
    while True:
        print('=========\n' +
              'Enter action to perform.\n' +
              '1. Create Multilogin Profile\n' +
              '2. Create Instagram Account\n' +
              '3. SignIn Instagram Account\n' +
              '4. Exit\n' +
              '=========\n')

        user_input = await ainput("Please enter your input: ")

        if user_input == '1':
            # Perform the action for creating a Multilogin profile
            jsonData = await HttpClient("http://localhost:3001").post("/profile/generate/5")
            logger.info(jsonData)
            # Your code for creating a Multilogin profile goes here

        elif user_input == '2':
            # Perform the action for creating an Instagram account
            print("Creating Instagram Account...")
            jsonData = await HttpClient("http://localhost:3001").get("/profile/unused")
            for profile in jsonData['profiles']:
                logger.info(profile['uuid'])
                bot = Automation(profile['uuid'])
                await bot.generate_instagram_account(env)
        elif user_input == '3':
            bot = Automation('dummyUUid')
            await bot.instagram_sign_in()

        elif user_input == '4':
            # Exit the program
            print("Exiting...")
            break

        else:
            # Handle invalid input
            print("Invalid input. Please try again.\n")


asyncio.run(main())
