from telegram import ext as tg
from aiohttp import ClientSession
from pyrogram import Client, errors
from telethon import TelegramClient
from TeamLegend.Config import *

import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGS = logging.getLogger("__name__")

updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
legendtbot = TelegramClient("Group_t_Bot", API_ID, API_HASH)

legendpbot = Client("Group_p_Bot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
dispatcher = updater.dispatcher
aiohttpsession = ClientSession()
