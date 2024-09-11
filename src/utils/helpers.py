import random
from .consts import comments
import asyncio
import logging
from pyrogram import Client

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors.exceptions import MessageNotModified


def generate_random_comment():
    n = random.randint(0, len(comments) - 1)

    return comments[n]

def get_phones_from_file(path):
    pass

def check_if_user_subscribed(client: Client, channel: int):
    pass


async def forward_mediaGroup(c_c, client: Client, message: Message):
    if not c_c["mediaGroup"]:
        c_c["mediaGroup"] = True
        mediagroup_with_entities = (await client.get_media_group(message.sender_chat.id, message.id)).pop()

        message_new = (
            await client.copy_media_group(
                c_c["to"],
                message.sender_chat.id,
                message.id,
            )
        ).pop()

        # print(message_new)

        text = mediagroup_with_entities.text if mediagroup_with_entities.text else mediagroup_with_entities.caption
        entities = (
            mediagroup_with_entities.entities
            if mediagroup_with_entities.entities
            else mediagroup_with_entities.caption_entities
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

        await asyncio.sleep(2)
        c_c["mediaGroup"] = False


async def forward_message(c_c, client: Client, message: Message):
    message_new = await client.copy_message(
        c_c["to"], message.sender_chat.id, message.id
    )

    text = message_new.text if message_new.text else message_new.caption
    entities = (
        message_new.entities if message_new.entities else message_new.caption_entities
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
