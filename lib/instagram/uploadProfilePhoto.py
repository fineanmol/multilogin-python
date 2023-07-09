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


async def upload_media_photo(browser, photo_path, caption):
    try:
        await asyncio.sleep(2)
        WebDriverWait(browser, 30)  # Maximum wait await asyncio of 30 seconds

        add_media_button = browser.find_element_by_xpath('//*[name()="svg"][@aria-label="New post"]')
        add_media_button.click()

        await asyncio.sleep(2)

        media_upload_btn = browser.find_element_by_xpath("//input[@type='file']")
        media_upload_btn.send_keys(photo_path)

        await asyncio.sleep(1)

        do_crop_next_btn = browser.find_element_by_xpath('//div[text()="Next"]')
        do_crop_next_btn.click()

        await asyncio.sleep(3)

        do_filter_next_btn = browser.find_element_by_xpath('//div[text()="Next"]')
        do_filter_next_btn.click()

        await asyncio.sleep(4)

        input_caption_field = browser.find_element_by_xpath("//div[contains(@aria-label, 'Write a caption...')]")
        for char in caption:
            input_caption_field.send_keys(char)
            await asyncio.sleep(0.5)
        await asyncio.sleep(3)

        share_btn = browser.find_element_by_xpath('//div[text()="Share"]')
        share_btn.click()

        await asyncio.sleep(10)


    except Exception as e:
        print(e)
