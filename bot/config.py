import os
import logging


# Database engine
ENGINE = {
    "url": "sqlite:///db.sqlite3",
    "echo": True,
}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d:%(levelname)s:[%(asctime)s] - %(name)s - %(message)s",
)

# Telegram token
API_TOKEN = os.getenv("API_TOKEN")

# Deepgram token and options
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
OPTIONS = {
    "punctuate": True,
    "language": "ru",
}
