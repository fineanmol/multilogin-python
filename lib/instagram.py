import asyncio
import aiohttp
import random
from logger import Logger

message = ''
time_left = ''
status = 1

logger = Logger()


async def signup(browser, user, profile_id):
    page = await browser.newPage()
    await page.goto('https://instagram.com/accounts/emailsignup/')

    await page.waitForSelector('input[name=emailOrPhone]', visible=True)
    await asyncio.sleep(0.3)
    await page.type('input[name=emailOrPhone]', user['number'], {'delay': 27})

    await asyncio.sleep(0.5)
    await page.type('input[name=fullName]', f"{user['firstName']} {user['lastName']}", {'delay': 82})

    await asyncio.sleep(0.7)
    username = await page.querySelectorEval('input[name=username]', 'el => el.value')
    if username:
        user['username'] = username
    else:
        await page.type('input[name=username]', user['username'], {'delay': 67})
    await page.keyboard.press('Tab')
    await asyncio.sleep(1)
    await page.keyboard.press('Space')
    await asyncio.sleep(0.3)

    await asyncio.sleep(0.3)
    await page.type('input[name=password]', user['password'], {'delay': 42})

    await asyncio.sleep(0.7)
    signup_button = await page.xpath('//button[@type="submit"]')
    user['username'] = await page.querySelectorEval('input[name=username]', 'el => el.value')

    await asyncio.sleep(4)

    async def add_account_data_to_profile():
        await asyncio.sleep(4)
        url = f"http://localhost:3001/profile/{profile_id}/addAccount"
        account_details = {
            'account': {
                'username': user['username'],
                'password': user['password'],
                'phoneNumber': user['number']
            }
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=account_details) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        logger.info('Account added to profile' + response_data)
                    else:
                        logger.error('Failed to add account to profile:' + response.status)
        except Exception as e:
            logger.error('Failed to add account to profile:' + str(e))

    async def fetch_otp_details():
        while status not in [0, 2, 3, 4, 5, 6]:
            try:
                await asyncio.sleep(3)
                sms_pool_fetch_api = 'https://api.smspool.net/sms/check'
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                            f"{sms_pool_fetch_api}?orderid={user['orderId']}&key={user['key']}") as response:
                        if response.status == 200:
                            json_data = await response.json()
                            message = str(json_data['sms'])
                            status = json_data['status']
                            time_left = json_data['time_left']
                            print('[OTP Response]', {'jsonData': json_data, 'message': message, 'timeLeft': time_left})
                            await asyncio.sleep(4)
                        else:
                            print('An error occurred while checking API status:', response.status)
                            break
            except Exception as e:
                print('An error occurred while checking API status:', str(e))
                break
        print('[Status of the API is]', status)

    await asyncio.gather(signup_button[0].click({'delay': 70}))

    await asyncio.sleep(5)

    def get_random_integer(min_val, max_val):
        return str(random.randint(min_val, max_val))

    await page.selectOption('select[title="Month:"]', get_random_integer(0, 12))
    await page.selectOption('select[title="Day:"]', get_random_integer(0, 29))
    await page.selectOption('select[title="Year:"]', get_random_integer(1965, 2000))
    await asyncio.sleep(5)
    next_buttons = await page.xpath('//button[@type="button"]')
    if len(next_buttons) > 0:
        await next_buttons[1].click()

    await fetch_otp_details()
    await page.waitForSelector('input[name=confirmationCode]', visible=True)
    await asyncio.sleep(0.3)
    if status != 1:
        await page.type('input[name=confirmationCode]', message, {'delay': 27})
        await asyncio.sleep(5)
        confirmation_signup_button = await page.xpath('//button[@type="button"]')
        if len(confirmation_signup_button) > 0:
            await confirmation_signup_button[0].click()
            await add_account_data_to_profile()

    await page.close()
