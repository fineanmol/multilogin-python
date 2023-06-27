import asyncio
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from logger import Logger

logger = Logger.get_instance()


def delay(seconds):
    time.sleep(seconds / 1000)


async def new_like_post(browser):
    # Scroll to load more buttons and continue liking
    counter = 1
    while True:
        await asyncio.sleep(4)
        try:
            posts = browser.find_elements_by_xpath("//article")
            for post in posts:
                element = post.find_element_by_xpath('//*[name()="svg"][@aria-label="Like"]')
                element.click()
                logger.info(counter)
                counter = counter + 1
                await asyncio.sleep(1)

            # Scroll to the end of the page
            browser.execute_script("arguments[0].scrollIntoView();", posts[-1])
            # Find articles again after scrolling
            posts = browser.find_elements(By.XPATH, "//article")
        except Exception as e:
            logger.info(e)

    # hm = browser.find_element_by_xpath(
    #     '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[1]/div/a')
    #
    # hm.click()
    #
    # await asyncio.sleep(4)
    #
    # for n in range(1, 1000):
    #
    #     try:
    #         nm = '//*[@id="react-root"]/section/main/section/div[1]/div[1]/div/article[' + str(
    #             n) + ']/div[2]/section[1]/span[1]/button'
    #
    #         follow = browser.find_element_by_xpath(nm)
    #         follow.click()
    #     except:
    #         pass


async def like_posts_handler(browser):
    try:
        scroll_step = 500  # Number of pixels to scroll
        scroll_delay = 1000  # Delay between each scroll step
        max_scroll_attempts = 10  # Maximum number of scroll attempts
        scroll_attempts = 0
        while scroll_attempts < max_scroll_attempts:
            browser.execute_script(f"window.scrollBy(0, {scroll_step})")
            await asyncio.sleep(4)

            posts = browser.find_elements_by_xpath("//article")

            for post in posts:
                like_button = post.find_element_by_css_selector("div > div:nth-child(3) > div > div > "
                                                                "div:nth-child(1)"
                                                                ">div:nth-child(1)>span>button")
                like_button.click()
                await asyncio.sleep(1)
            scroll_attempts = scroll_attempts + 100
    # for item in range(1, 101):
    #     xPathStart = '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/section/div/div[3]/div/div/div[1]/div/article['
    #     variablePath = item
    #     xPathEnd = ']/div/div[3]/div/div/section[1]/span[1]/button'
    #     elements = browser.find_elements_by_xpath('//div[@class="_abm0 _abl_"]/span/svg[@aria-label="Like"]')
    #
    #     delay(700)
    #
    #     like_buttons = browser.find_elements_by_xpath(f"{xPathStart}{variablePath}{xPathEnd}")
    #     print({ "length": len(like_buttons),elements:len(elements) })
    #
    #     if like_buttons:
    #         like_buttons[0].click()
    #         # Rest of your code using the 'like_button' variable
    #
    #     else:
    #         # Scroll to the next set of elements
    #         scroll_attempts = 0
    #         while scroll_attempts < max_scroll_attempts:
    #             browser.execute_script(f"window.scrollBy(0, {scroll_step})")  # Scroll vertically by 'scroll_step' pixels
    #
    #             delay(scroll_delay)
    #             delay(500)
    #
    #             updated_like_buttons = browser.find_elements_by_xpath(f"{xPathStart}[{variablePath}]{xPathEnd}")
    #             delay(200)
    #
    #             if updated_like_buttons:
    #                 updated_like_buttons[0].click()
    #                 # Rest of your code using the 'like_button' variable
    #                 print({ "Liked Pressed": len(updated_like_buttons) })
    #                 break  # Exit the loop after a successful button click
    #
    #             scroll_attempts += 1

    except Exception as err:
        print(err)


async def like_post(browser):
    try:
        # Go to the Instagram feed
        browser.get('https://instagram.com')
        delay(2000)

        # button_notification = browser.find_element_by_xpath('//button[text()="Not Now"]')
        # button_notification.click()

        await new_like_post(browser)

    except Exception as err:
        print(err)
