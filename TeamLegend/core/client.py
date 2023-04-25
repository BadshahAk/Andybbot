from LegendGB.core.logging import LOGS

import telegram.ext as tg
from aiohttp import ClientSession
from pyrogram import Client, errors
from telethon import TelegramClient
from TeamLegend.Config import *

updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
legendtbot = TelegramClient("Kannadiga", API_ID, API_HASH)

legendpbot = Client("KannadigaBot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
dispatcher = updater.dispatcher
aiohttpsession = ClientSession()
