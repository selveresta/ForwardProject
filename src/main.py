import asyncio
from threading import Thread
from client.client import TelegramClient
from config.config import API_HASH, API_ID, PHONE
from utils.logger import create_logger

# from pyrogram import idle
from pyrogram.methods.utilities.idle import idle

create_logger()

client = TelegramClient("listener", API_ID, API_HASH, PHONE, True, False)
client_commentator = TelegramClient(
    "commentator", API_ID, API_HASH, "+380687028385", False, True
)


async def start_clients():
    # loop = asyncio.get_event_loop()
    # run = loop.run_until_complete
    # Start both clients
    await client.client.start()
    print("Client 1 started")

    await client_commentator.client.start()
    print("Client 2 started")

    # Keep both clients running
    # await asyncio.gather(client.idle(), client_commentator.idle())
    # run(idle())


async def stop_clients():
    # Stop both clients
    await client.client.stop()
    await client_commentator.client.stop()


def main():
    loop = asyncio.get_event_loop()

    try:
        # Start clients and run event loop
        # asyncio.run()
        loop.run_until_complete(start_clients())
        loop.run_until_complete(idle())

        # loop.run_forever()  # Keeps the loop running until interrupted
    except Exception as e:
        print(e)
    finally:

        print("KeyboardInterrupt received: Stopping clients...")
        loop.run_until_complete(stop_clients())
        # asyncio.run(stop_clients())
        loop.close()  # Ensure loop is properly closed
        # Stop clients gracefully
        print("Event loop closed")


# # Run the clients

# if __name__ == "__main__":
#     try:
#         asyncio.run(run_clients())  # This method automatically handles loop management
#     except KeyboardInterrupt:
#         print("Program interrupted")

if __name__ == "__main__":
    main()
#     loop = asyncio.get_event_loop()
#     try:
#         loop.run_until_complete(start_clients())
#     except KeyboardInterrupt:
#         loop.run_until_complete(stop_clients())
# asyncio.run(client.start_client())
# asyncio.run(client_commentator.start_client())
# loop = asyncio.get_event_loop()


# def startup(client: TelegramClient):
#     asyncio.run_coroutine_threadsafe(client.start_client, loop)


# thread1 = Thread(target=startup, args=[client])
# thread2 = Thread(target=startup, args=[client_commentator])

# thread1.start()
# thread2.start()
