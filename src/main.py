import asyncio

from client.client import client
from config.config import API_HASH, API_ID, PHONE
from utils.logger import create_logger


create_logger()

client.run()
