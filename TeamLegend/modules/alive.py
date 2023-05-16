from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram import __version__ as telever
from telethon import __version__ as tlhver

from TeamLegend import BOT_NAME, BOT_USERNAME
from TeamLegend.core.clients import legendpbot

ALIVE_PIC = "https://graph.org/file/f60051408d17fd505fa11.jpg"
@legendpbot.on_message(filters.command("alive"))
async def awake(_, message: Message):
    TEXT = f"**Hey {message.from_user.mention},\n\nI Am {BOT_NAME}**\n━━━━━━━━━━━━━━━━━━\n\n"
    TEXT += f"» **This Bot Is For [Team Legend](https://t.me/TeamLegendXD)\n\n"
    TEXT += f"» **Telegram Version :** `{telever}` \n\n"
    TEXT += f"» **Telethon Version :** `{tlhver}` \n\n"
    TEXT += f"» **Pyrogram Version :** `{pyrover}` \n━━━━━━━━━━━━━━━━━\n\n"
    BUTTON = [
        [
            InlineKeyboardButton("ʜᴇʟᴘ", url=f"https://t.me/{BOT_USERNAME}?start=help"),
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/TeamLegendXD"),
        ]
    ]
    await message.reply_photo(
        photo=ALIVE_PIC,
        caption=TEXT,
        reply_markup=InlineKeyboardMarkup(BUTTON),
    )

    
__help__ = """
*alive* is used to check bot is on or not

*🔰 User Commands:*

☞ /alive : _Check Bot is on or not_
"""

__mod_name__ = "Alive"
