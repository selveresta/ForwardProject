import asyncio
from client.TG import PyrogramClient
from client.TG import TelethonClient
from telethon import events
from telethon.tl.custom import Message
from config.config import API_HASH, API_ID, PHONE
from pyrogram import idle
from channels.channels import (
    source_destination_channels_map as sdcm,
)
import logging
import asyncio


class MessageForwarder:
    """
    This class integrates Telethon and Pyrogram clients.
    Telethon listens to messages in specific groups, and Pyrogram copies those messages.
    """

    def __init__(
        self,
        pyrogram_client: PyrogramClient,
        telethon_client: TelethonClient,
        group_ids: list,
        destination_chat_id: int,
    ):
        self.pyrogram_client = pyrogram_client
        self.telethon_client = telethon_client
        self.group_ids = group_ids  # List of group IDs to listen to
        self.destination_chat_id = destination_chat_id  # Chat ID to forward messages to

    async def telethon_listener(self):
        """
        Attaches a message handler to the Telethon client to listen for messages in specified groups.
        """

        @self.telethon_client.client.on(events.NewMessage())
        async def handler(event: events.NewMessage.Event):
            message: Message = event.message  # Extract the message object

            message = event.message
            c_c = self.get_current_from(message)

            if not c_c:
                logging.error(f"Chat ID - {message.chat_id}; Found channel - {c_c}")
                return

            logging.info(f"New message in group {message.chat_id}: {message.text}")

            if c_c["mediaGroup"]:
                return
            # Use Pyrogram to copy the message to the destination chat
            await self.copy_message_to_destination(
                message, c_c, True if message.grouped_id else False
            )

    async def copy_message_to_destination(self, message: Message, c_c, isMG: bool):
        """
        Copies the message from the Telethon client to the destination chat using Pyrogram.
        """

        try:

            if isMG:
                c_c["mediaGroup"] = True
                await self.pyrogram_client.client.copy_media_group(
                    chat_id=int(c_c["to"]),  # Destination chat
                    from_chat_id=int(message.chat_id),  # Source chat ID
                    message_id=int(message.id),  # Message ID to copy
                )

                await asyncio.sleep(3)
                c_c["mediaGroup"] = False
            else:
                await self.pyrogram_client.client.copy_message(
                    chat_id=int(c_c["to"]),  # Destination chat
                    from_chat_id=int(message.chat_id),  # Source chat ID
                    message_id=int(message.id),  # Message ID to copy
                )

            logging.info(
                f"Message copied successfully from {message.chat_id} to {self.destination_chat_id}"
            )
        except Exception as e:
            logging.error(f"Failed to copy message: {str(e)}")

    async def run(self):
        # Start the message listener in the background
        await self.telethon_listener()

        """
        Run both Telethon and Pyrogram clients.
        """
        ptask = asyncio.create_task(self.pyrogram_client.run_client())
        ttask = asyncio.create_task(self.telethon_client.run_client())
        await ptask
        await ttask
        # Keep both clients alive
        # await asyncio.gather(
        #     ptask,
        #     ttask,
        # )

    def get_current_from(self, message: Message):
        c_id = message.chat_id

        for k, v in sdcm.items():
            if c_id == v["from"]:
                return v

        return None
