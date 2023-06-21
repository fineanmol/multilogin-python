from faker import Faker

from lib.automation import Automation
from logger import Logger
from constant import services

fake = Faker()
service_list = services.ServiceList()
logger = Logger()


bot = Automation("53dd9d87-f1fa-4115-8af4-7910bc3cd1ba")

bot.generate_instagram_account()
