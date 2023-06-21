import asyncio
from aioconsole import ainput

from lib.automation import Automation
from logger import Logger

from httpClient import HttpClient
logger = Logger.get_instance()


async def main():
    while True:
        print('=========\n' +
              'Enter action to perform.\n' +
              '1. Create Multilogin Profile\n' +
              '2. Create Instagram Account\n' +
              '3. Exit\n' +
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
                await bot.generate_instagram_account()

        elif user_input == '3':
            # Exit the program
            print("Exiting...")
            break

        else:
            # Handle invalid input
            print("Invalid input. Please try again.\n")

asyncio.run(main())
