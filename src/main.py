# import asyncio
# from threading import Thread
# from client.client import CustomTelegramClient
# from config.config import API_HASH, API_ID, PHONE
# from utils.logger import create_logger


# create_logger()

# client = CustomTelegramClient("listener", API_ID, API_HASH, PHONE, True, False)
# client_commentator = CustomTelegramClient(
#     "commentator", API_ID, API_HASH, "+380687028385", False, True
# )


# async def start_clients():
#     # Start both clients
#     await client.client.start()
#     print("Client 1 started")

#     await client_commentator.client.start()
#     print("Client 2 started")

#     # Keep both clients running
#     await asyncio.gather(client.idle(), client_commentator.idle())


# async def stop_clients():
#     # Stop both clients
#     await client.client.stop()
#     await client_commentator.client.stop()


# def main():
#     loop = asyncio.get_event_loop()

#     try:
#         # Start clients and run event loop
#         loop.run_until_complete(start_clients())
#         loop.run_forever()  # Keeps the loop running until interrupted

#     except KeyboardInterrupt:
#         print("KeyboardInterrupt received: Stopping clients...")
#         loop.run_until_complete(stop_clients())  # Stop clients gracefully
#     finally:
#         loop.close()  # Ensure loop is properly closed
#         print("Event loop closed")


# # # Run the clients

# # if __name__ == "__main__":
# #     try:
# #         asyncio.run(run_clients())  # This method automatically handles loop management
# #     except KeyboardInterrupt:
# #         print("Program interrupted")

# if __name__ == "__main__":
#     main()
# #     loop = asyncio.get_event_loop()
# #     try:
# #         loop.run_until_complete(start_clients())
# #     except KeyboardInterrupt:
# #         loop.run_until_complete(stop_clients())
# # asyncio.run(client.start_client())
# # asyncio.run(client_commentator.start_client())
# # loop = asyncio.get_event_loop()


# # def startup(client: TelegramClient):
# #     asyncio.run_coroutine_threadsafe(client.start_client, loop)


# # thread1 = Thread(target=startup, args=[client])
# # thread2 = Thread(target=startup, args=[client_commentator])

# # thread1.start()
# # thread2.start()


# Main async function to run both clients


# import asyncio
# from client.TG import PyrogramClient, TelethonClient
# from config.config import API_HASH, API_ID, PHONE
# from pyrogram import idle


# async def main():
#     # Pyrogram setup
#     pyrogram_client = PyrogramClient(
#         api_id=API_ID, api_hash=API_HASH, session_name="pclient", phone=PHONE
#     )
#     await pyrogram_client.create_client()

#     # Telethon setup, pass Pyrogram client to Telethon
#     telethon_client = TelethonClient(
#         api_id=API_ID,
#         api_hash=API_HASH,
#         session_string="tclient",
#         phone=PHONE,
#         pyrogram_client=pyrogram_client.client,
#     )
#     await telethon_client.create_client()

#     # Run both clients asynchronously
#     asyncio.create_task(pyrogram_client.run_client())  # Run Pyrogram in the background
#     asyncio.create_task(telethon_client.run_client())  # Run Telethon in the background


# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
from client.TG import PyrogramClient
from client.TG import TelethonClient
from client.MessageForward import MessageForwarder
from telethon import events
from telethon.tl.custom import Message
from config.config import API_HASH, API_ID, PHONE
from pyrogram import idle
from channels.channels import (
    source_destination_channels_map as sdcm,
)
from utils.logger import create_logger


create_logger()

async def main():
    # Pyrogram configuration
    pyrogram_client = PyrogramClient(
        api_id=API_ID, api_hash=API_HASH, session_name="pclient", phone=PHONE
    )

    await pyrogram_client.create_client()
    # Telethon configuration
    telethon_client = TelethonClient(
        api_id=API_ID,
        api_hash=API_HASH,
        session_string="tclient",
        phone=PHONE,
        pyrogram_client=pyrogram_client.client,
    )

    await telethon_client.create_client()
    # List of group IDs to listen to
    group_ids = [-1002247420892, -1002191626337, -1001616247897]  # Example group IDs

    # Destination chat ID (e.g., your own chat or another group)
    destination_chat_id = (
        -1002202360303
    )  # Replace with actual chat ID where you want to forward the messages

    # Create an instance of the MessageForwarder
    forwarder = MessageForwarder(
        pyrogram_client, telethon_client, group_ids, destination_chat_id
    )

    # Start both clients and message forwarding
    try:
        await forwarder.run()
    except asyncio.CancelledError:
        await pyrogram_client.client.stop()
        await telethon_client.client.disconnect()
        raise


if __name__ == "__main__":
    asyncio.run(main())
