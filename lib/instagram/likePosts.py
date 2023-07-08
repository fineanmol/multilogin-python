import asyncio
import random
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from lib.instagram.signin import signin
from logger import Logger

logger = Logger.get_instance()


async def delay(seconds):
    await asyncio.sleep(seconds)


async def new_like_post(browser):
    # Scroll to load more buttons and continue liking
    counter = 1
    while True:
        await asyncio.sleep(4)
        try:
            posts = browser.find_elements(By.XPATH, "//article")
            for i in range(len(posts)):
                try:
                    post = posts[i]
                    element = post.find_element(By.XPATH, '//*[name()="svg"][@aria-label="Like"]')
                    element.click()
                    logger.info(f"Liked post {counter}")
                    counter += 1
                    await asyncio.sleep(1)
                except Exception as ex:
                    logger.error(f"Failed to click like button: {ex}")

                # Scroll to the next post
                if i < len(posts) - 1:
                    next_post = posts[i + 1]
                    browser.execute_script("arguments[0].scrollIntoView({ behavior: 'instant', block: 'center' });",
                                           next_post)

            # Find articles again after scrolling
            posts = browser.find_elements(By.XPATH, "//article")
        except Exception as e:
            logger.error(f"Failed to find articles: {e}")


async def like_posts_handler(browser, required_count):
    try:
        global counter
        scroll_step = 125  # Number of pixels to scroll
        scroll_delay = 2  # Delay between each scroll step
        max_scroll_attempts = 500  # Maximum number of scroll attempts

        await delay(4)
        wait = WebDriverWait(browser, 10)

        # Scroll to the next set of elements
        scroll_attempts = 0

        while scroll_attempts < max_scroll_attempts:
            browser.execute_script(f"window.scrollBy(0, {scroll_step})")  # Scroll vertically by 'scroll_step' pixels
            await delay(scroll_delay)
            try:
                like_buttons = wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[name()="svg"][@aria-label="Like"]')))
                username_fetch = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@role="link"]')))
                print({"length": len(like_buttons), "scroll attempts": scroll_attempts})

                if like_buttons:
                    for i in range(len(like_buttons)):
                        await delay(1)
                        like_buttons[i].click()
                        counter += 1
                        print({"Liked Pressed": counter, "username": str(username_fetch[i].text)})

                        if counter >= required_count:
                            print(f"Reached the session limit of {required_count}. Exiting session...")
                            return  # Exit the function, which will lead to terminating the session

            except StaleElementReferenceException:
                print("Stale Element Reference Exception occurred. Retrying...")

            scroll_attempts += 1
    except Exception as err:
        print("Error, Like Button Click Failed")
        print("Message:", str(err) if str(err) else "Unknown Error")
        await like_posts_handler(browser, required_count)


async def like_post(browser, required_count):
    try:
        # Go to the Instagram feed
        await delay(2)
        await like_posts_handler(browser, required_count)

    except Exception as err:
        print(err)


async def like_post_run_program(browser, daily_limit):
    session_count = 3  # Number of sessions per day
    session_duration = 3600  # Duration of each session in seconds
    session_limits = []  # List to store the session limits
    session_logs = []  # List to store session details for logging

    remaining_limit = daily_limit
    for _ in range(session_count - 1):
        session_limit = random.randint(10, remaining_limit - (session_count - 1))
        session_limits.append(session_limit)
        remaining_limit -= session_limit
    session_limits.append(remaining_limit)

    # browser = webdriver.Chrome()  # Instantiate your preferred browser driver
    # Login to Instagram or perform any necessary setup
    # await signin(browser)

    session_number = 1
    for session_limit in session_limits:
        print(f"Running session {session_number} with limit {session_limit}")
        start_time = datetime.now()
        await like_post(browser, daily_limit, session_limit)
        end_time = datetime.now()

        session_logs.append({
            "session_number": session_number,
            "session_limit": session_limit,
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "likes_done": counter
        })

        session_number += 1
        if counter >= daily_limit:
            print("Reached the daily limit. Exiting...")
            break

        remaining_time = session_duration - (end_time - start_time).total_seconds()
        if remaining_time > 0:
            print(f"Waiting for {remaining_time} seconds until the next session...")
            await delay(remaining_time)

    browser.quit()

    print("Program execution completed.")

    # Logging session details
    with open('session.log', 'a') as log_file:
        log_file.write("\nSession Logs:\n")
        for log in session_logs:
            log_file.write(f"\nSession {log['session_number']} - Likes Done: {log['likes_done']}\n")
            log_file.write(f"Start Time: {log['start_time']}\n")
            log_file.write(f"End Time: {log['end_time']}\n")


counter = 0  # Global counter for tracking likes
# asyncio.run(run_program(daily_limit))
