import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Configuration settings
class Config:
    TOKEN = os.getenv('DISCORD_TOKEN')
    PREFIX = '!'  # Command prefix