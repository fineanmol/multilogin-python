import asyncio
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from lib.instagram.likePosts import like_post
from lib.instagram.followAccounts import follow_accounts
import pickle

from lib.instagram.updateBio import update_profile_bio
from logger import Logger

logger = Logger.get_instance()


# Save cookies to a file
def save_cookie(browser, filename):
    cookies = browser.get_cookies()
    with open(f'{filename}-cookies.pkl', 'wb') as file:
        pickle.dump(cookies, file)


def load_cookie(browser, filename):
    try:
        with open(f'{filename}-cookies.pkl', 'rb') as file:
            cookies = pickle.load(file)
            # Add the cookies to the WebDriver
            for cookie in cookies:
                browser.add_cookie(cookie)
    except FileNotFoundError:
        print("Cookie not found")
    except IOError:
        print("An error occurred while reading cookies file")
    except Exception as e:
        print("An unexpected error occurred:", str(e))


async def signin(browser):
    user = {
        'email': 'jasonford468',
        'password': ')7Y9sxfJJ&4Q'
    }
    browser.get('https://instagram.com')
    await asyncio.sleep(2)
    load_cookie(browser, user['email'])
    browser.get('https://instagram.com')
    try:
        accept_cookies_button = browser.find_element_by_xpath('//button[text()="Allow all cookies"]')
        accept_cookies_button.click()
    except Exception as e:
        logger.info("Accept cookie button not found!")
    # Check if element with id "myElement" exists
    elements = browser.find_elements_by_xpath('//button[contains(.,"Log in")]')
    if len(elements) > 0:
        logger.info("Not logged In")
        # Wait until the elements are present
        wait = WebDriverWait(browser, 30)  # Maximum wait time of 30 seconds
        input_email_or_phone = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name=username]")))
        input_email_or_phone.send_keys(user.get('email') or user.get('username'))

        password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name=password]")))
        password.send_keys(user.get('password'))

        signin_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"Log in")]')))
        signin_button.click()
        await asyncio.sleep(4)

        time.sleep(5)
        logger.info('Login Success, Ready for the next step..')
        try:
            save_your_login_info_button = browser.find_element_by_xpath('//button[@type="button"]')
            save_your_login_info_button.click()
        except:
            logger.info("Save Login Details Popup not available")
    else:
        logger.info("Already Logged In")
        time.sleep(2)
    try:
        button_notification = browser.find_element_by_xpath('//button[text()="Not Now"]')
        button_notification.click()
    except:
        logger.info("Turn On Notification popup not found")
    await asyncio.sleep(2)
    save_cookie(browser, user['email'])
    await asyncio.sleep(10)
    quote = "Embrace the journey, chase your dreams, and let your story inspire others."
    await update_profile_bio(user.get('email'), user.get('password'), quote, browser)
    # await like_post(browser)
    # await follow_accounts(browser)
    browser.quit()
