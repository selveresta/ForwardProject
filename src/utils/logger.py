import logging


def create_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("./bot.log"),  # Log to a file
            logging.StreamHandler(),  # Log to console
        ],
    )
