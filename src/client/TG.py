import abc
import asyncio
from pyrogram import Client as PyrogramClientLib, filters, idle
from pyrogram.types import Message
from telethon import TelegramClient as TelethonClientLib, events
from telethon.sessions import StringSession
from enum import Enum
from channels.channels import (
    source_destination_channels_map as sdcm,
)
from pyrogram.errors.exceptions import MessageNotModified
from telethon.tl.custom import Message as TMessage

import logging
class ClientType(Enum):
    Pyrogram = "P"
    Telethon = "T"


class TelegramClientBase(abc.ABC):
    """
    Abstract base class for Telegram clients.
    It defines the methods for creating and running clients asynchronously.
    """

    @abc.abstractmethod
    async def create_client(self):
        """
        Abstract method to create and configure the client.
        """
        pass

    @abc.abstractmethod
    async def run_client(self):
        """
        Abstract method to run the client in an async loop.
        """
        pass


class PyrogramClient(TelegramClientBase):
    """
    Concrete class that implements TelegramClientBase using Pyrogram.
    """

    def __init__(self, api_id: int, api_hash: str, session_name: str, phone: str):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_name = session_name
        self.phone = phone
        self.client = None

    async def create_client(self):
        """
        Creates the Pyrogram client instance.
        """
        self.client = PyrogramClientLib(
            self.session_name,
            api_id=self.api_id,
            api_hash=self.api_hash,
            phone_number=self.phone,
        )

        # # Define a handler to respond to incoming messages
        # @self.client.on_message(filters.me)
        # async def handle_message(client, message: Message):
        #     print(f"Pyrogram Received Message: {message.text}")

    async def run_client(self):
        """
        Starts the Pyrogram client in an async loop.
        """
        await self.client.start()
        logging.info("Pyrogram Client Running...")

        # Keep the bot running asynchronously
        # await idle()  # Keeps the bot alive until interrupted


class TelethonClient(TelegramClientBase):
    """
    Concrete class that implements TelegramClientBase using Telethon.
    """

    client: TelethonClientLib

    def __init__(
        self,
        api_id: int,
        api_hash: str,
        session_string: str,
        phone: str,
        pyrogram_client: PyrogramClientLib,
    ):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_string = session_string
        self.phone = phone
        self.pyrogram_client = pyrogram_client  # Pyrogram client instance
        self.client = None

    async def create_client(self):
        """
        Creates the Telethon client instance.
        """
        async with TelethonClientLib(
            self.session_string, self.api_id, self.api_hash
        ) as client:
            self.client = client
        # Define a handler for incoming messages in Telethon
        # @self.client.on(events.NewMessage(outgoing=True))
        # async def forward_message_channel(event):
        #     message: TMessage = event.message
        #     c_c = self.get_current_from(message)

        #     if not c_c:
        #         return

        #     await self.forward_message(c_c, self.pyrogram_client, message)

        # if message.media_group_id:
        #     await self.forward_message(c_c, self.pyrogram_client, message)
        # if not c_c["mediaGroup"]:
        #     c_c["mediaGroup"] = True
        #     message_new = await client.copy_media_group(
        #         c_c["to"],
        #         message.sender_chat.id,
        #         message.id,
        #     )
        #     await asyncio.sleep(2)
        #     c_c["mediaGroup"] = False
        # else:
        # message_new = await client.copy_message(
        #     c_c["to"], message.sender_chat.id, message.id
        # )

        # text = message_new.text if message_new.text else message_new.caption
        # entities = (
        #     message_new.entities
        #     if message_new.entities
        #     else message_new.caption_entities
        # )
        # try:
        #     await client.edit_message_caption(
        #         c_c["to"],
        #         message_new.id,
        #         text,
        #         caption_entities=entities,
        #     )
        # except MessageNotModified as e:
        #     print(f"Error - {e}")

    async def run_client(self):
        """
        Starts the Telethon client in an async loop.
        """
        await self.client.start()
        logging.info("Telethon Client Running...")

        # Keep the client running in a loop
        await self.client.run_until_disconnected()  # Keeps the client alive until disconnected

    def get_current_from(self, message: TMessage):
        c_id = message.chat_id
        for k, v in sdcm.items():
            if c_id == v["from"]:
                return v

        return None

    async def forward_message(self, c_c, client: PyrogramClientLib, message: TMessage):
        message_new = await client.copy_message(c_c["to"], message.chat_id, message.id)

        text = message_new.text if message_new.text else message_new.caption
        entities = (
            message_new.entities
            if message_new.entities
            else message_new.caption_entities
        )
        try:
            await client.edit_message_caption(
                c_c["to"],
                message_new.id,
                text,
                caption_entities=entities,
            )
        except MessageNotModified as e:
            print(f"Error - {e}")
