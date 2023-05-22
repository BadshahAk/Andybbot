
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
GET_ME = dispatcher.get_me()
BOT_ID = GET_ME.id
BOT_NAME = GET_ME.first_name
BOT_USERNAME = GET_Me.username




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
