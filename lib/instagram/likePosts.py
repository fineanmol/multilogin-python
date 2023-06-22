import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def delay(seconds):
    time.sleep(seconds / 1000)


def like_posts_handler(browser):
    try:
        scroll_step = 500  # Number of pixels to scroll
        scroll_delay = 1000  # Delay between each scroll step
        max_scroll_attempts = 10  # Maximum number of scroll attempts

        for item in range(1, 101):
            xPathStart = '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/section/div/div[3]/div/div/div[1]/div/article['
            variablePath = item
            xPathEnd = ']/div/div[3]/div/div/section[1]/span[1]/button'
            elements = browser.find_elements_by_xpath('//div[@class="_abm0 _abl_"]/span/svg[@aria-label="Like"]')

            delay(700)

            like_buttons = browser.find_elements_by_xpath(f"{xPathStart}{variablePath}{xPathEnd}")
            print({ "length": len(like_buttons),elements:len(elements) })

            if like_buttons:
                like_buttons[0].click()
                # Rest of your code using the 'like_button' variable

            else:
                # Scroll to the next set of elements
                scroll_attempts = 0
                while scroll_attempts < max_scroll_attempts:
                    browser.execute_script(f"window.scrollBy(0, {scroll_step})")  # Scroll vertically by 'scroll_step' pixels

                    delay(scroll_delay)
                    delay(500)

                    updated_like_buttons = browser.find_elements_by_xpath(f"{xPathStart}[{variablePath}]{xPathEnd}")
                    delay(200)

                    if updated_like_buttons:
                        updated_like_buttons[0].click()
                        # Rest of your code using the 'like_button' variable
                        print({ "Liked Pressed": len(updated_like_buttons) })
                        break  # Exit the loop after a successful button click

                    scroll_attempts += 1

    except Exception as err:
        print(err)


def like_post(browser):
    try:
        # Go to the Instagram feed
        browser.get('https://instagram.com')
        delay(2000)

        turn_on_notification_buttons = browser.find_elements_by_xpath('/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[1]')

        if turn_on_notification_buttons:
            turn_on_notification_buttons[0].click()
            print('[Turn on Notification, Yes Clicked]')

        like_posts_handler(browser)

    except Exception as err:
        print(err)
