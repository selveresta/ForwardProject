import os
from dotenv import load_dotenv

load_dotenv()

API_ID = str(os.environ.get("API_ID", 0))
API_HASH = str(os.environ.get("API_HASH", 0))
PHONE = str(os.environ.get("PHONE", 0))
OPENAI_API_KEY = str(os.environ.get("OPENAI_API_KEY", 0))


profiles = []

def generate_profiles():
    file_data = 0

def generate_listener_profiles(file_data):
    pass

def generate_comentators_profiles():
    pass