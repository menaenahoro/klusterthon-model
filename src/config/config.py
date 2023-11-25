import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONNECTOR = os.getenv('DATABASE_CONNECTOR')
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')
SQS_QUEUE_URL_DS = os.getenv('SQS_QUEUE_URL_DS')
SQS_QUEUE_URL_UI = os.getenv('SQS_QUEUE_URL_UI')
SQS_QUEUE_URL_BE = os.getenv('SQS_QUEUE_URL_BE')
SQS_QUEUE_URL_FE = os.getenv('SQS_QUEUE_URL_FE')
SQS_QUEUE_URL_PM = os.getenv('SQS_QUEUE_URL_PM')
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
GROUP_URL = os.getenv('GROUP_URL')
GROUP_BEARER_TOKEN = os.getenv('GROUP_BEARER_TOKEN')
