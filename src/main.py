import asyncio

from client.client import TelegramClient
from config.config import API_HASH, API_ID, PHONE
from utils.logger import create_logger


create_logger()

client = TelegramClient("forwardProject", API_ID, API_HASH, PHONE)
client.start_client()