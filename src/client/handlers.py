import asyncio
import logging
from pyrogram import Client
from channels.channels import (
    source_destination_channels_map as sdcm,
)
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors.exceptions import MessageNotModified


def get_current_from(message: Message):
    c_id = message.chat.id
    for k, v in sdcm.items():
        if c_id == v["from"]:
            return v

    return None


async def forward_message_channel(client: Client, message: Message):
    c_c = get_current_from(message)
    logging.info(message)
    if not c_c:
        return

    if message.media_group_id:
        if not c_c["mediaGroup"]:
            c_c["mediaGroup"] = True
            await client.copy_media_group(
                c_c["to"],
                message.sender_chat.id,
                message.id,
            )

            await asyncio.sleep(2)

            send_comment_to_post(client, message)
            c_c["mediaGroup"] = False
    else:
        message_new = await client.copy_message(
            c_c["to"], message.sender_chat.id, message.id
        )

        text = message_new.text if message_new.text else message_new.caption
        try:
            await client.edit_message_caption(
                c_c["to"],
                message_new.id,
                text,
            )

            send_comment_to_post(client, message)
        except MessageNotModified as e:
            print(e)


async def send_comment_to_post(client: Client, message: Message):
    m = await client.get_discussion_message(message.chat.id, message.id)
    logging.info(m)
    # text = message.text if message.text else message.caption
    # print(text)
    # comments = gpt.generate_comments_by_post(text)
    # await asyncio.sleep(groups_to_comment[group_comment_test]["delay"])
    await m.reply("comment")
