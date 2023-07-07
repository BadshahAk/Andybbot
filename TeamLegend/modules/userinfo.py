import html
import os
import re

import requests
from telegram import (
    MAX_MESSAGE_LENGTH,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
)
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import escape_markdown, mention_html

import TeamLegend.sql.userinfo_sql as sql
from TeamLegend.Config import DEV_USERS
from TeamLegend import INFOPIC
from TeamLegend.core.clients import dispatcher
from TeamLegend.__main__ import STATS, TOKEN, USER_INFO
from TeamLegend.modules.disable import DisableAbleCommandHandler
from TeamLegend.helpers.chat_status import user_admin
from TeamLegend.helpers.extraction import extract_user
from TeamLegend.sql.afk_sql import check_afk_status, is_afk
from TeamLegend.sql.global_bans_sql import is_user_gbanned
from TeamLegend.sql.users_sql import get_user_num_chats


def no_by_per(totalhp, percentage):
    """
    rtype: num of `percentage` from total
    eg: 1000, 10 -> 10% of 1000 (100)
    """
    return totalhp * percentage / 100


def get_percentage(totalhp, earnedhp):
    """
    rtype: percentage of `totalhp` num
    eg: (1000, 100) will return 10%
    """

    matched_less = totalhp - earnedhp
    per_of_totalhp = 100 - matched_less * 100.0 / totalhp
    per_of_totalhp = str(int(per_of_totalhp))
    return per_of_totalhp


def hpmanager(user):
    total_hp = (get_user_num_chats(user.id) + 10) * 10

    if not is_user_gbanned(user.id):
        # Assign new var `new_hp` since we need `total_hp` in
        # end to calculate percentage.
        new_hp = total_hp

        # if no username decrease 25% of hp.
        if not user.username:
            new_hp -= no_by_per(total_hp, 25)
        try:
            dispatcher.bot.get_user_profile_photos(user.id).photos[0][-1]
        except IndexError:
            # no profile photo ==> -25% of hp
            new_hp -= no_by_per(total_hp, 25)
        # if no /setme exist ==> -20% of hp
        if not sql.get_user_me_info(user.id):
            new_hp -= no_by_per(total_hp, 20)
        # if no bio exsit ==> -10% of hp
        if not sql.get_user_bio(user.id):
            new_hp -= no_by_per(total_hp, 10)

        if is_afk(user.id):
            afkst = check_afk_status(user.id)
            # if user is afk and no reason then decrease 7%
            # else if reason exist decrease 5%
            if not afkst.reason:
                new_hp -= no_by_per(total_hp, 7)
            else:
                new_hp -= no_by_per(total_hp, 5)

        # fbanned users will have (2*number of fbans) less from max HP
        # Example: if HP is 100 but user has 5 diff fbans
        # Available HP is (2*5) = 10% less than Max HP
        # So.. 10% of 100HP = 90HP

    # Commenting out fban health decrease cause it wasnt working and isnt needed ig.
    # _, fbanlist = get_user_fbanlist(user.id)
    # new_hp -= no_by_per(total_hp, 2 * len(fbanlist))

    # Bad status effects:
    # gbanned users will always have 5% HP from max HP
    # Example: If HP is 100 but gbanned
    # Available HP is 5% of 100 = 5HP

    else:
        new_hp = no_by_per(total_hp, 5)

    return {
        "earnedhp": int(new_hp),
        "totalhp": int(total_hp),
        "percentage": get_percentage(total_hp, new_hp),
    }


def make_bar(per):
    done = min(round(per / 10), 10)
    return "■" * done + "□" * (10 - done)



def get_id(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    msg = update.effective_message
    user_id = extract_user(msg, args)

    if user_id:
        if msg.reply_to_message and msg.reply_to_message.forward_from:
            user1 = message.reply_to_message.from_user
            user2 = message.reply_to_message.forward_from

            msg.reply_text(
                f"<b>Tᴇʟᴇɢʀᴀᴍ Iᴅ:</b>,"
                f"• {html.escape(user2.first_name)} - <code>{user2.id}</code>.\n"
                f"• {html.escape(user1.first_name)} - <code>{user1.id}</code>.",
                parse_mode=ParseMode.HTML,
            )

        else:
            user = bot.get_chat(user_id)
            msg.reply_text(
                f"{html.escape(user.first_name)}'s ɪᴅ ɪs <code>{user.id}</code>.",
                parse_mode=ParseMode.HTML,
            )

    else:
        if chat.type == "private":
            msg.reply_text(
                f"Yᴏᴜʀ Usᴇʀ ɪᴅ ɪs <code>{chat.id}</code>.", parse_mode=ParseMode.HTML
            )

        else:
            msg.reply_text(
                f"Tʜɪs Gʀᴏᴜᴩ's ɪᴅ ɪs <code>{chat.id}</code>.", parse_mode=ParseMode.HTML
            )


@user_admin
def group_info(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat

    if args and len(args) >= 1:
            try:
                connect_chat = int(args[0])

            except ValueError:
                try:
                    connect_chat = str(args[0])
                    get_chat = context.bot.getChat(connect_chat)
                    connect_chat = get_chat.id

                except BadRequest:
                    bot.send_message(update.effective_message, "Invalid Chat ID!")
                    return
            except BadRequest:
                bot.send_message(update.effective_message, "Invalid Chat ID!")
                return
            entity = bot.get_chat(connect_chat)
            totaladmin = bot.get_chat_administrators(entity.id)
            msg = f"*Group info of* - `{entity.title}`\n" 
            msg += f"\n*ID*: `{entity.id}`"
            msg += f"\n*Title*: `{entity.title}`"
            msg += f"\n*Description*: `{entity.description}`"
            msg += f"\n*Supergroup*: `{entity.type}`"
            msg += f"\n*Can Send*: `{entity.permissions.can_send_messages}`"
            msg += f"\n*Bio*: `{entity.bio}`"
            msg += f"\n*Slowmode*: `{entity.slow_mode_delay}`"
            msg += f"\n*Location*: `{entity.location}`"
            if entity.username:
                msg += f"\n**Username*: @{entity.username}"
            msg += "\n\n*Member Stats:*"
            msg += f"\n`Admins:` `{len(totaladmin)}`"
            if entity.invite_link:
                msg += f"\n*Link*: {entity.invite_link}"
            message.reply_text(msg, parse_mode=ParseMode.HTML)

    else:
            entity = bot.get_chat(chat.id)
            totaladmin = bot.get_chat_administrators(entity.id)
            msg = f"**Group info of** - `{entity.title}`\n" 
            msg += f"\n**ID**: `{entity.id}`"
            msg += f"\n**Title**: `{entity.title}`"
            msg += f"\n**Description**: `{entity.description}`"
            msg += f"\n**Supergroup**: `{entity.type}`"
            msg += f"\n**Can Send**: `{entity.permissions.can_send_messages}`"
            msg += f"\n**Bio**: `{entity.bio}`"
            msg += f"\n**Slowmode**: `{entity.slow_mode_delay}`"
            msg += f"\n**Location**: `{entity.location}`"
            if entity.username:
                msg += f"\n**Username**: {entity.username}"
            msg += "\n\n**Member Stats:**"
            msg += f"\n`Admins:` `{len(totaladmin)}`"
            if entity.invite_link:
                msg += f"\n**Link**: {entity.invite_link}"
            message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)



def gifid(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.animation:
        update.effective_message.reply_text(
            f"Gif ID:\n<code>{msg.reply_to_message.animation.file_id}</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text("Please reply to a gif to get its ID.")



def info(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    user_id = extract_user(update.effective_message, args)

    if user_id:
        user = bot.get_chat(user_id)

    elif not message.reply_to_message and not args:
        user = message.from_user

    elif not message.reply_to_message and (
        not args
        or (
            len(args) >= 1
            and not args[0].startswith("@")
            and not args[0].isdigit()
            and not message.parse_entities([MessageEntity.TEXT_MENTION])
        )
    ):
        message.reply_text("I can't extract a user from this.")
        return

    else:
        return

    rep = message.reply_text("<code>ᴀᴩᴩʀᴀɪsɪɴɢ...</code>", parse_mode=ParseMode.HTML)

    text = (
        f"ㅤ ㅤㅤ      ✦ Usᴇʀ Iɴғᴏ ✦\n•❅─────✧❅✦❅✧─────❅•\n"
        f"➻ <b>Usᴇʀ Iᴅ:</b> <code>{user.id}</code>\n"
        f"➻ <b>Fɪʀsᴛ Nᴀᴍᴇ:</b> {html.escape(user.first_name)}"
    )

    if user.last_name:
        text += f"\n➻ <b>Lᴀsᴛ Nᴀᴍᴇ:</b> {html.escape(user.last_name)}"

    if user.username:
        text += f"\n➻ <b>Usᴇʀɴᴀᴍᴇ:</b> @{html.escape(user.username)}"

    text += f"\n➻ <b>Lɪɴᴋ:</b> {mention_html(user.id, 'link')}"

    if chat.type != "private" and user_id != bot.id:
        _stext = "\n➻ <b>ᴩʀᴇsᴇɴᴄᴇ:</b> <code>{}</code>"

        afk_st = is_afk(user.id)
        if afk_st:
            text += _stext.format("AFK")
        else:
            status = status = bot.get_chat_member(chat.id, user.id).status
            if status:
                if status in {"left", "kicked"}:
                    text += _stext.format("ɴᴏᴛ ʜᴇʀᴇ")
                elif status == "member":
                    text += _stext.format("ᴅᴇᴛᴇᴄᴛᴇᴅ")
                elif status in {"administrator", "creator"}:
                    text += _stext.format("ᴀᴅᴍɪɴ")
    if user_id not in [bot.id, 777000]:
        userhp = hpmanager(user)
        text += f"\n\n<b>Hᴇᴀʟᴛʜ:</b> <code>{userhp['earnedhp']}/{userhp['totalhp']}</code>\n[<i>{make_bar(int(userhp['percentage']))} </i>{userhp['percentage']}%]"

    if user.id == OWNER_ID:
        text += "\n\nᴛʜᴇ ᴅɪsᴀsᴛᴇʀ ʟᴇᴠᴇʟ ᴏғ ᴛʜɪs ᴜsᴇʀ ɪs <b>ɢᴏᴅ</b>.\n"
    elif user.id in DEV_USERS:
        text += "\n\nᴛʜɪs ᴜsᴇʀ ɪs ᴀ ᴍᴇᴍʙᴇʀ ᴏғ <b>ᴀɴᴏɴ ᴀssᴏᴄɪᴀᴛɪᴏɴ</b>.\n"
    try:
        user_member = chat.get_member(user.id)
        if user_member.status == "administrator":
            result = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={chat.id}&user_id={user.id}"
            )
            result = result.json()["result"]
            if "custom_title" in result.keys():
                custom_title = result["custom_title"]
                text += f"\n\nTɪᴛʟᴇ:\n<b>{custom_title}</b>"
    except BadRequest:
        pass

    for mod in USER_INFO:
        try:
            mod_info = mod.__user_info__(user.id).strip()
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id).strip()
        if mod_info:
            text += "\n\n" + mod_info

    if INFOPIC:
        try:
            profile = context.bot.get_user_profile_photos(user.id).photos[0][-1]
            _file = bot.get_file(profile["file_id"])
            _file.download(f"{user.id}.png")
            IPHOTO = open(f"{user.id}.png", "rb")
            message.reply_photo(
                IPHOTO,
                caption=(text),
                parse_mode=ParseMode.HTML,
                
            )
            os.remove(f"{user.id}.png")
        # Incase user don't have profile pic, send normal text
        except IndexError:
            message.reply_text(
                text, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            )

    else:
        message.reply_text(
            text, parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )

    rep.delete()


@sudo_plus
def stats(update: Update, context: CallbackContext):
    stats = "<b>🧐 Cᴜʀʀᴇɴᴛ sᴛᴀᴛs :</b>\n\n" + "\n".join([mod.__stats__() for mod in STATS])
    result = re.sub(r"(\d+)", r"<code>\1</code>", stats)
    update.effective_message.reply_text(result, parse_mode=ParseMode.HTML)



def __user_info__(user_id):
    bio = html.escape(sql.get_user_bio(user_id) or "")
    me = html.escape(sql.get_user_me_info(user_id) or "")
    result = ""
    if me:
        result += f"<b>ᴀʙᴏᴜᴛ ᴜsᴇʀ:</b>\n{me}\n"
    if bio:
        result += f"<b>ᴏᴛʜᴇʀs sᴀʏ ᴛʜᴀᴛ:</b>\n{bio}\n"
    result = result.strip("\n")
    return result


__help__ = """
✘ *User Commands*:
 ➣ /id*:* get the current group id. If used by replying to a message, gets that user's id.
 ➣ /gifid*:* reply to a gif to me to tell you its file ID.
 ➣ /info*:* get information about a user. 

 ✘ *Dev Users*:
 ➣ /grpinfo*:* Get all details about this group
 ➣ /stats*:* Get Stats about me
"""


STATS_HANDLER = CommandHandler("stats", stats)
ID_HANDLER = DisableAbleCommandHandler("id", get_id)
GIFID_HANDLER = DisableAbleCommandHandler("gifid", gifid)
INFO_HANDLER = DisableAbleCommandHandler(("info"), info)
GINFO_HANDLER = DisableAbleCommandHandler("grpinfo", group_info)


dispatcher.add_handler(STATS_HANDLER)
dispatcher.add_handler(ID_HANDLER)
dispatcher.add_handler(GIFID_HANDLER)
dispatcher.add_handler(INFO_HANDLER)
dispatcher.add_handler(GINFO_HANDLER)

__mod_name__ = "Infos"
__command_list__ = ["info", "id", "grpinfo", "stats", "gifid"]
__handlers__ = [
    ID_HANDLER,
    GIFID_HANDLER,
    INFO_HANDLER,
    GINFO_HANDLER,
    STATS_HANDLER,
]
