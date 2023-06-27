import asyncio
import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from logger import Logger

logger = Logger.get_instance()


async def delay(seconds):
    await asyncio.sleep(seconds)


counter = 0


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
                    browser.execute_script("arguments[0].scrollIntoView({ behavior: 'instant', block: 'center' });", next_post)

            # Find articles again after scrolling
            posts = browser.find_elements(By.XPATH, "//article")
        except Exception as e:
            logger.error(f"Failed to find articles: {e}")


async def like_posts_handler(browser):
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
                username_fetch = wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, '//a[@role="link"]/span/div')))
                print({"length": len(like_buttons), "scroll attempts": scroll_attempts})

                if like_buttons:
                    for i in range(len(like_buttons)):
                        await delay(1)
                        like_buttons[i].click()
                        counter += 1
                        print({"Liked Pressed": counter, "username": str(username_fetch[i].text)})

                        if counter >= 100:
                            print("Reached 100 likes. Exiting...")
                            return  # Exit the function, which will lead to program termination

            except StaleElementReferenceException:
                print("Stale Element Reference Exception occurred. Retrying...")

            scroll_attempts += 1
    except Exception as err:
        print("Error, Like Button Click Failed")
        print("Message:", str(err) if str(err) else "Unknown Error")
        await like_posts_handler(browser)


async def like_post(browser):
    try:
        # Go to the Instagram feed
        await delay(2)
        #await like_posts_handler(browser)
        await new_like_post(browser)
    except Exception as err:
        print(err)
