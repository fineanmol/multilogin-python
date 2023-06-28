import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

async def update_profile_bio(username, password, quote,browser):
    try:
        await asyncio.sleep(2)
        wait = WebDriverWait(browser, 30)  # Maximum wait await asyncio of 30 seconds

        # Go to the profile page
        profile_link = browser.find_element(By.XPATH, "//a[@href='/" + username + "/']")
        profile_link.click()
        await asyncio.sleep(2)

        # Click the "Edit Profile" button
        edit_profile_button = browser.find_element_by_xpath('//a[text()="Edit Profile"]')
        edit_profile_button.click()
        await asyncio.sleep(3)
        try:
            account_center_button = browser.find_element_by_xpath('//div[@role="button"]')
            if(len(account_center_button)>0):
                cross_btn = account_center_button[1].click()
        except:
            print('Account Center Button Not Found')

        # Clear the existing bio and update it with the random quote
        bio_textarea = browser.find_element(By.XPATH, "//textarea")
        bio_textarea.clear()
        bio_textarea.send_keys(quote)

        # Save the updated profile bio
        submit_button = browser.find_element(By.XPATH, "//div[text()='Submit']")
        await asyncio.sleep(2)
        submit_button.click()

        print("Profile bio updated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        browser.quit()

async def upload_profile_photo(browser):
    try:
        await asyncio.sleep(2)
        wait = WebDriverWait(browser, 30)  # Maximum wait await asyncio of 30 seconds

        # Go to the profile page
        profile_link = browser.find_element(By.XPATH, "//a[@href='/" + "jasonford468" + "/']")
        profile_link.click()
        await asyncio.sleep(2)

        # Click the "Edit Profile" button
        edit_profile_button = browser.find_element_by_xpath('//a[text()="Edit Profile"]')
        edit_profile_button.click()
        await asyncio.sleep(3)

        upload_photo_btn = browser.find_element_by_xpath("//input[@type='file']")
        upload_photo_btn.send_keys("/Users/nnishad/PythonProjects/multilogin-python/LinkedIn_icon.png")

    except Exception as e:
        print(e)