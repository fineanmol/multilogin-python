import asyncio
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from logger import Logger

logger = Logger.get_instance()

async def follow_accounts(browser,follow_count):
    try:
        username = 'johncena'
        followerUsernameXPathStart = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[' \
                                     '2]/div/div/div[2]/div[1]/div/div['
        followerUsernameXPathEnd = ']/div/div/div/div[2]/div/div/span[1]/span/div/div/div/a'
        scrollStep = 500  # Number of pixels to scroll
        scrollDelay = 1  # Delay between each scroll step
        maxScrollAttempts = 10  # Maximum number of scroll attempts

        # Go to profile browser
        browser.get(f"https://instagram.com/{username}/")
        # Wait until the elements are present
        wait = WebDriverWait(browser, 30)  # Maximum wait time of 30 seconds

        await asyncio.sleep(4)

        try:
            browser.find_element_by_xpath("//div[text()='Follow']").click()
        except:
            logger.info("Looks like already following.")
        await asyncio.sleep(2)

        # Go to profile browser
        browser.get(f"https://instagram.com/{username}/")
        await asyncio.sleep(3)
        # Click on followers button
        followersBtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"a[href='/{username}/followers/']")))
        followersBtn.click()
        await asyncio.sleep(5)

        # Scrape follower data
        for item in range(1, follow_count):
            try:
                follow_buttons = browser.find_elements_by_xpath('//button[@type="button" and div="Follow"]')
                if follow_buttons:
                    follow_button = follow_buttons[0]
                    follow_button.click()
                time.sleep(2)
                cancel_unfollow = browser.find_element_by_xpath('//button[text()="Cancel"]')
                if cancel_unfollow:
                    cancel_unfollow.click()
                follower_names = False
                if follower_names and False:
                    follower_name = follower_names[0]
                    follower_text = follower_name.text
                    current_date = time.time()
                    timestamp = int(round(current_date * 1000))
                    follower_data = {
                        'followerUsername': follower_text,
                        'timestamp': timestamp
                    }
                    print({'followerData': follower_data})
                    # Store the 'followerData' object in your database
                else:
                    # Scroll to the next set of elements
                    scroll_attempts = 0
                    while scroll_attempts < maxScrollAttempts:
                        browser.execute_script(
                            f"window.scrollBy(0, {scrollStep})")  # Scroll vertically by 'scrollStep' pixels
                        time.sleep(scrollDelay / 1000)

                        updated_follow_buttons = browser.find_elements_by_xpath(
                            '//button[@type="button" and div="Follow"]')
                        cancel_unfollow = browser.find_element_by_xpath('//button[text()="Cancel"]')
                        if cancel_unfollow:
                            cancel_unfollow.click()
                        if updated_follow_buttons:
                            follow_button = updated_follow_buttons[0]
                            follow_button.click()
                            break  # Exit the loop after a successful button click

                        scroll_attempts += 1

                time.sleep(2)  # Delay between each iteration of the loop

            except Exception as e:
                print("Unexpected exception:", e)
                # Handle the exception accordingly

    except Exception as e:
        print("Outer exception:", e)
        # Handle the exception accordingly
