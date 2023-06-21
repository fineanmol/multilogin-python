from faker import Faker
from faker.providers import internet

from lib.automation import Automation
from logger import Logger
from constant import services
import asyncio

fake = Faker()
service_list = services.ServiceList()
logger = Logger()
loop = asyncio.get_event_loop()

bot = Automation("53dd9d87-f1fa-4115-8af4-7910bc3cd1ba")

loop.run_until_complete(bot.generate_instagram_account())
fake.add_provider(internet)

print(fake.simple_profile())
loop.close()