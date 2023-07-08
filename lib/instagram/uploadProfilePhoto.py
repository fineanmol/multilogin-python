import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


async def upload_profile_photo(browser, photo_path):
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
        upload_photo_btn.send_keys(photo_path)

    except Exception as e:
        print(e)
