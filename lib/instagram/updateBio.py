import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def update_profile_bio(username, password, quote):
    try:
        # Start the WebDriver and go to Instagram
        driver = webdriver.Chrome()
        driver.get("https://www.instagram.com/")
        time.sleep(2)

        # Log in to Instagram
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys(username)
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(password)
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        time.sleep(2)

        # Close the "Save Your Login Info" prompt if it appears
        save_info_button = driver.find_element(By.XPATH, "//button[text()='Not Now']")
        save_info_button.click()
        time.sleep(2)

        # Close the "Turn On Notifications" prompt if it appears
        notifications_button = driver.find_element(By.XPATH, "//button[text()='Not Now']")
        notifications_button.click()
        time.sleep(2)

        # Go to the profile page
        profile_link = driver.find_element(By.XPATH, "//a[@href='/" + username + "/']")
        profile_link.click()
        time.sleep(2)

        # Click the "Edit Profile" button
        edit_profile_button = driver.find_element(By.XPATH, "//button[text()='Edit Profile']")
        edit_profile_button.click()
        time.sleep(2)

        # Clear the existing bio and update it with the random quote
        bio_textarea = driver.find_element(By.XPATH, "//textarea[@aria-label='Bio']")
        bio_textarea.clear()
        bio_textarea.send_keys(quote)

        # Save the updated profile bio
        submit_button = driver.find_element(By.XPATH, "//button[text()='Submit']")
        submit_button.click()
        time.sleep(2)

        print("Profile bio updated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Quit the WebDriver
        driver.quit()

# Example usage
username = "your_username"
password = "your_password"
quote = "This is a random quote. Update your bio with meaningful content."
update_profile_bio(username, password, quote)
