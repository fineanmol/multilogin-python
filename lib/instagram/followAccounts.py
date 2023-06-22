import time
from selenium import webdriver


async def follow_accounts(browser, user):
    try:
        username = 'vindiesel'
        xPathStart = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div['
        xPathEnd = ']/div/div/div/div[3]/div/button/div/div'
        followerUsernameXPathStart = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div['
        followerUsernameXPathEnd = ']/div/div/div/div[2]/div/div/span[1]/span/div/div/div/a'
        scrollStep = 500  # Number of pixels to scroll
        scrollDelay = 1000  # Delay between each scroll step
        maxScrollAttempts = 10  # Maximum number of scroll attempts

        # Go to profile browser
        browser.get(f"https://instagram.com/{username}/")
        time.sleep(1)

        # Click on followers button
        browser.wait_for_selector(f"a[href='/{username}/followers/']")
        browser.click(f"a[href='/{username}/followers/']")
        time.sleep(1)

        # Scrape follower data
        for item in range(1, 101):
            follow_buttons = browser.xpath(f"{xPathStart}{item}{xPathEnd}")
            if follow_buttons:
                follow_button = follow_buttons[0]
                # Rest of your code using the 'follow_button' variable
                follow_button.click()
            time.sleep(2)

            follower_names = browser.xpath(f"{followerUsernameXPathStart}{item}{followerUsernameXPathEnd}")
            if follower_names:
                follower_name = follower_names[0]
                follower_text = follower_name.text
                current_date = time.time()
                timestamp = int(round(current_date * 1000))
                follower_data = {
                    'followerUsername': follower_text,
                    'timestamp': timestamp
                }
                print({ 'followerData': follower_data })
                # Store the 'followerData' object in your database
            else:
                # Scroll to the next set of elements
                scroll_attempts = 0
                while scroll_attempts < maxScrollAttempts:
                    browser.execute_script(f"window.scrollBy(0, {scrollStep})")  # Scroll vertically by 'scrollStep' pixels
                    time.sleep(scrollDelay / 1000)

                    updated_follow_buttons = browser.xpath(f"{xPathStart}{item}{xPathEnd}")
                    if updated_follow_buttons:
                        follow_button = updated_follow_buttons[0]
                        # Rest of your code using the 'follow_button' variable
                        follow_button.click()
                        break  # Exit the loop after a successful button click

                    scroll_attempts += 1

            time.sleep(2)  # Delay between each iteration of the loop

    except Exception as err:
        print(err)
