import asyncio

from pyrogram import Client
from pyrogram import filters
from config.config import API_HASH, API_ID, PHONE
from channels.channels import (
    source_destination_channels_map,
    channel_name_Rektology,
    group_comment_test,
    groups_to_comment,
)
from pyrogram import Client
from pyrogram.types import Message
from deep_translator import GoogleTranslator
from pyrogram.errors.exceptions import MessageNotModified
from api.GPTClient import gpt
from pyrogram.handlers import MessageHandler

channels = source_destination_channels_map


async def forward_message_channel(client: Client, message: Message):
    if message.media_group_id:
        if not channels[channel_name_Rektology][2]:
            channels[channel_name_Rektology][2] = True
            await client.copy_media_group(
                channels[channel_name_Rektology][1],
                message.sender_chat.id,
                message.id,
            )

            await asyncio.sleep(2)
            channels[channel_name_Rektology][2] = False
    else:
        message_new = await client.copy_message(
            channels[channel_name_Rektology][1], message.sender_chat.id, message.id
        )

        text = message_new.text if message_new.text else message_new.caption
        try:
            await client.edit_message_caption(
                channels[channel_name_Rektology][1],
                message_new.id,
                text,
            )
        except MessageNotModified as e:
            print(e)


async def send_comment_to_post(client: Client, message: Message):
    print(message)
    m = await client.get_discussion_message(message.chat.id, message.id)

    # text = message.text if message.text else message.caption
    # print(text)
    # comments = gpt.generate_comments_by_post(text)
    # await asyncio.sleep(groups_to_comment[group_comment_test]["delay"])
    await m.reply("comment")
