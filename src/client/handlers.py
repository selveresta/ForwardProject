import asyncio
import logging
from pyrogram import Client
from channels.channels import (
    source_destination_channels_map as sdcm,
)
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors.exceptions import MessageNotModified, MessageIdInvalid

from utils.helpers import forward_mediaGroup, forward_message, generate_random_comment
from main import client


def get_current_from(message: Message):
    c_id = message.chat.id
    for k, v in sdcm.items():
        if c_id == v["from"]:
            return v

    return None


async def forward_message_channel(client: Client, message: Message):
    c_c = get_current_from(message)

    if not c_c:
        return

    if message.media_group_id:
        await forward_mediaGroup(c_c, client, message)
        # if not c_c["mediaGroup"]:
        #     c_c["mediaGroup"] = True
        #     message_new = await client.copy_media_group(
        #         c_c["to"],
        #         message.sender_chat.id,
        #         message.id,
        #     )
        #     await asyncio.sleep(2)
        #     c_c["mediaGroup"] = False
    else:
        await forward_message(c_c, client, message)
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


async def forward_message_channel1(event):
    message = event.message
    c_c = get_current_from(message)

    if not c_c:
        return

    if message.media_group_id:
        await forward_mediaGroup(c_c, client, message)
        # if not c_c["mediaGroup"]:
        #     c_c["mediaGroup"] = True
        #     message_new = await client.copy_media_group(
        #         c_c["to"],
        #         message.sender_chat.id,
        #         message.id,
        #     )
        #     await asyncio.sleep(2)
        #     c_c["mediaGroup"] = False
    else:
        await forward_message(c_c, client, message)
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


async def send_comment_to_post(client: Client, message: Message):
    try:
        await asyncio.sleep(5)
        m = await client.get_discussion_message(message.chat.id, message.id)
        # text = message.text if message.text else message.caption
        # print(text)
        comment = generate_random_comment()

        # await asyncio.sleep(groups_to_comment[group_comment_test]["delay"])
        await m.reply(comment)
    except MessageIdInvalid as miie:
        return
    except Exception as e:
        logging.error(e)
