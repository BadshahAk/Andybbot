import sys
import time
from telegram import ext as tg
from aiohttp import ClientSession
from pyrogram import Client, errors
from telethon import TelegramClient
from TeamLegend.core.clients import *
from TeamLegend.Config import *
StartTime = time.time()


# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGS.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1) 


print("[INFO]: Getting Bot Info...")

BOT_ID = dispatcher.bot.id
BOT_NAME = dispatcher.bot.first_name
BOT_USERNAME = dispatcher.bot.username


# Aʙᴏᴜᴛ Oᴡɴᴇʀ
owner_name = "『𖤍 Lêɠêɳ̃dẞογ ࿐』➙「🇮🇳」"
owner_tg = "https://t.me/LegendBoyOP"
owner_id = 5591734243
"""
# Load at end to ensure all prev variables have been set
from TeamLegend.helpers.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
"""
