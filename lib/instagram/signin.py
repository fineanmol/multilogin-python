import asyncio
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from lib.instagram.likePosts import like_post
from lib.instagram.followAccounts import follow_accounts
from lib.instagram.updateBio import update_profile_bio


async def signin(browser):
    user = {
        'email': 'jasonford468',
        'password': ')7Y9sxfJJ&4Q'
    }
    browser.get('https://instagram.com')
    await asyncio.sleep(10)

    # Wait until the elements are present
    wait = WebDriverWait(browser, 30)  # Maximum wait time of 30 seconds
    input_email_or_phone = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name=username]")))
    input_email_or_phone.send_keys(user.get('email') or user.get('username'))

    password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name=password]")))
    password.send_keys(user.get('password'))

    signin_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"Log in")]')))
    await asyncio.sleep(2)
    signin_button.click()

    await asyncio.sleep(3)
    try:
        try:
            save_your_login_info_button = browser.find_element_by_xpath('//button[@type="button"]')
            if save_your_login_info_button.is_displayed():
                save_your_login_info_button.click()
        except Exception as err:
            print('Error:', 'save_your_login_info_button NOT FOUND')

        print('Login Success, Ready for the next step..\n')
        await asyncio.sleep(3)
        button_notification = browser.find_element_by_xpath('//button[text()="Not Now"]')
        button_notification.click()
       
    except Exception as err:
        print('Error:', "button_notification NOT FOUND")

    quote="Embrace the journey, chase your dreams, and let your story inspire others."
    await update_profile_bio(user.get('email'),user.get('password'), quote, browser)
    # await like_post(browser)
    # await follow_accounts(browser)
  
