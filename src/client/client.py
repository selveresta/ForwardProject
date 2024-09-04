import asyncio

from pyrogram import Client
from pyrogram import filters
from config.config import API_HASH, API_ID, PHONE
from channels.channels import (
    source_destination_channels_map as sdcm,
    groups_to_comment as gtc,
)
from pyrogram import Client
from pyrogram.types import Message
from deep_translator import GoogleTranslator
from pyrogram.errors.exceptions import MessageNotModified
from api.GPTClient import gpt
from pyrogram.handlers import MessageHandler
from .handlers import forward_message_channel, send_comment_to_post


class TelegramClient:
    client: Client

    def __init__(self, name, api_id, api_hash, phone_number):
        self.client = Client(
            name=name, api_id=api_id, api_hash=api_hash, phone_number=phone_number
        )
        self.register_client_handler()

    def start_client(self):
        self.client.run()

    def get_channels_ids(self):
        ids = []

        for k, v in sdcm.items():
            if v.get("from", None) and not v.get("users", None):
                ids.append(v["from"])
        return ids

    def get_channels_ids_from_user(self):
        ids = []
        users = []

        for k, v in sdcm.items():
            if v.get("from", None) and v.get("users", None):
                ids.append(v["from"])
                users.append(v["users"])
        return [ids, users]

    def get_channels_to_comment(self):
        ids = []

        for k, v in gtc.items():
            if v.get("id", None):
                ids.append(v["id"])

        return ids

    def register_client_handler(self):
        ids = self.get_channels_ids()
        ids_users = self.get_channels_ids_from_user()

        comments_ids = self.get_channels_to_comment()

        self.client.add_handler(
            MessageHandler(
                forward_message_channel,
                filters=filters.chat(ids),
            )
        )

        self.client.add_handler(
            MessageHandler(
                forward_message_channel,
                filters=filters.chat(ids_users[0]) & filters.user(ids_users[1]),
            )
        )

        self.client.add_handler(
            MessageHandler(
                send_comment_to_post,
                filters=filters.chat(comments_ids),
            )
        )


# @client.on_message(filters=filters.chat(channels[channel_name_Rektology][0]))
# async def forward_message_channel(client: Client, message: Message):
#     if message.media_group_id:
#         if not channels[channel_name_Rektology][2]:
#             channels[channel_name_Rektology][2] = True
#             await client.copy_media_group(
#                 channels[channel_name_Rektology][1], message.sender_chat.id, message.id
#             )

#             await asyncio.sleep(2)
#             channels[channel_name_Rektology][2] = False
#     else:
#         message_new = await client.copy_message(
#             channels[channel_name_Rektology][1], message.sender_chat.id, message.id
#         )

#         text = message_new.text if message_new.text else message_new.caption
#         try:
#             await client.edit_message_caption(
#                 channels[channel_name_Rektology][1],
#                 message_new.id,
#                 text,
#             )
#         except MessageNotModified as e:
#             print(e)


# @client.on_message(filters=filters.chat(groups_to_comment[group_comment_test]["id"]))
# async def send_comment_to_post(client: Client, message: Message):
#     # m = await client.get_discussion_message(message.chat.id, message.id)

#     text = message.text if message.text else message.caption
#     print(text)
#     comments = gpt.generate_comments_by_post(text)
#     # await asyncio.sleep(groups_to_comment[group_comment_test]["delay"])
#     # await m.reply("comment")
