import os

from aiogram.types import Message, File
from deepgram import Deepgram
from pathlib import Path


DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
MIMETYPE = "ogg"


deepgram = Deepgram(DEEPGRAM_API_KEY)


async def handle_file(message: Message, file: File, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)

    await message.bot.download_file(
        file_path=file.file_path, destination=f"{path}/{file_name}"
    )


async def transcript(file_path: str):
    options = {
        "punctuate": True,
        "language": "ru",
    }

    with open(f"{file_path}", "rb") as f:
        source = {"buffer": f, "mimetype": "audio/ogg"}
        result = await deepgram.transcription.prerecorded(source, options)
        return result["results"]["channels"][0]["alternatives"][0]["transcript"]
