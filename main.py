import asyncio
import os

from aioconsole import ainput

from httpClient import HttpClient
from lib.automation import Automation
from logger import Logger

logger = Logger.get_instance()


async def main():
    actions = {
        '1': create_multilogin_profile,
        '2': create_instagram_account,
        '3': run_scheduler,
        '4': modify_scheduler,
        '5': exit_program,
        '6': crawl,
        '7': upload_profile_photo,
        '8': upload_media
    }

    while True:
        print('=========\n' +
              'Enter action to perform.\n' +
              '1. Create Multilogin Profile\n' +
              '2. Create Instagram Account\n' +
              '3. Run Instagram Warmup\n' +
              '4. Modify Instagram Warmup Schedule\n' +
              '5. Exit\n' +
              '6. Crawl\n' +
              '7. Profile Photo Upload\n' +
              '8. Media Photo Upload\n' +
              '=========\n')

        user_input = input("Please enter your input: ")

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
        await bot.generate_instagram_account()


async def sign_in_instagram_account():
    bot = Automation('dummyUUid')
    await bot.sign_in_to_instagram()


async def run_scheduler():
    bot = Automation('dummyUUid')
    # await bot.sign_in_to_instagram()
    # await schedule_and_execute_tasks(bot)


async def modify_scheduler():
    bot = Automation('dummyUUid')
    # await bot.instagram_sign_in()


def exit_program():
    print("Exiting...")
    raise SystemExit


async def crawl():
    jsonData = await HttpClient("http://localhost:3001").get("/profile/unused")
    for profile in jsonData['profiles']:
        logger.info(profile['uuid'])
        bot = Automation(profile['uuid'])
        await bot.create_browser_history()


async def upload_profile_photo():
    bot = Automation("")
    await bot.instagram_upload_profile_photo("/Users/nikhil_nishad/Develop/python/multilogin-python/LinkedIn_icon.png")


async def upload_media():
    bot = Automation("")
    await bot.instagram_upload_media_photo()


asyncio.run(main())
