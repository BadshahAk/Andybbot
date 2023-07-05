import html
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Filters, run_async
from telegram.utils.helpers import mention_html

from TeamLegend import owner_name, owner_tg
from TeamLegend.Config import DEV_USERS, OWNER_ID
from TeamLegend.core.clients import dispatcher
from TeamLegend.modules.disable import DisableAbleCommandHandler
from TeamLegend.helpers.admin_rights import user_can_changeinfo
from TeamLegend.helpers.alternate import send_message
from TeamLegend.helpers.chat_status import (
    ADMIN_CACHE,
    bot_admin,
    can_pin,
    can_promote,
    connection_status,
    user_admin,
)
from TeamLegend.helpers.extraction import (
    extract_user,
    extract_user_and_text,
)
from TeamLegend.modules.log_channel import loggable
from TeamLegend.helpers.alternate import typing_action

@typing_action
@bot_admin
@user_admin
def set_sticker(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    if str(user.id) not in str(OWNER_ID):
        return msg.reply_text(
            "☞ Oɴʟʏ [owner_name](owner_tg) Hᴀᴠᴇ Pᴇʀᴍɪssɪᴏɴ ᴛᴏ Cʜᴀɴɢᴇ Tʜᴇ Sᴛɪᴄᴋᴇʀ Oғ Tʜᴇ Gʀᴏᴜᴘ",
            parse_mode=ParseMode.MARKDOWN,
        )

    if msg.reply_to_message:
        if not msg.reply_to_message.sticker:
            return msg.reply_text(
                "» Rᴇᴘʟʏ Tᴏ A Sᴛɪᴄᴋᴇʀ Tᴏ Sᴇᴛ As Gʀᴏᴜᴘ Sᴛɪᴄᴋᴇʀ !"
            )
        stkr = msg.reply_to_message.sticker.set_name
        try:
            context.bot.set_chat_sticker_set(chat.id, stkr)
            msg.reply_text(f"» Sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ Gʀᴏᴜᴘ Sᴛɪᴄᴋᴇʀ ɪɴ {chat.title}!")
        except BadRequest as excp:
            if excp.message == "Participants_too_few":
                return msg.reply_text(
                    f"» Yᴏᴜʀ Gʀᴏᴜᴘ Nᴇᴇᴅ Mɪɴɪᴍᴜᴍ 100 Mᴇᴍʙᴇʀ ᴛᴏ sᴇᴛ sᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ ɪɴ {chat.title}!"
                )
            msg.reply_text(f"Error ! {excp.message}.")
    else:
        msg.reply_text("» Rᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ sᴇᴛ ᴛᴏ sᴇᴛ ᴀs ɢʀᴏᴜᴘ sᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ !")



@bot_admin
@user_admin
def setchatpic(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user

    if str(user.id) not in str(OWNER_ID):
        return msg.reply_text(
            "☞ Oɴʟʏ [owner_name](owner_tg) Hᴀᴠᴇ Pᴇʀᴍɪssɪᴏɴ ᴛᴏ Cʜᴀɴɢᴇ Tʜᴇ Gʀᴏᴜᴘ Pɪᴄ!",
            parse_mode=ParseMode.MARKDOWN,
        )

    if msg.reply_to_message:
        if msg.reply_to_message.photo:
            pic_id = msg.reply_to_message.photo[-1].file_id
        elif msg.reply_to_message.document:
            pic_id = msg.reply_to_message.document.file_id
        else:
            return msg.reply_text("☞ You can set only photos as group photo !")

        dlmsg = msg.reply_text("» Changing group profile pic...")
        tpic = context.bot.get_file(pic_id)
        tpic.download("gpic.png")
        try:
            with open("gpic.png", "rb") as chatp:
                context.bot.set_chat_photo(int(chat.id), photo=chatp)
                msg.reply_text(f"» Successfully set group profile pic in {chat.title}!")
        except BadRequest as excp:
            msg.reply_text(f"Error ! {excp.message}")
        finally:
            dlmsg.delete()
            if os.path.isfile("gpic.png"):
                os.remove("gpic.png")
    else:
        msg.reply_text("» Reply to a photo or file photo to set as Group pic!")


@bot_admin
@user_admin
def rmchatpic(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user

    if str(user.id) not in str(OWNER_ID):
        return msg.reply_text(
            "☞ Oɴʟʏ [owner_name](owner_tg) Hᴀᴠᴇ Pᴇʀᴍɪssɪᴏɴ ᴛᴏ Cʜᴀɴɢᴇ Tʜᴇ Sᴛɪᴄᴋᴇʀ Oғ Tʜᴇ Gʀᴏᴜᴘ"
        )
    try:
        context.bot.delete_chat_photo(int(chat.id))
        msg.reply_text(f"» Successfully deleted default Group Profile pic")
      
    except BadRequest as excp:
        msg.reply_text(f"ᴇʀʀᴏʀ ! {excp.message}.")
        return



@bot_admin
@user_admin
def set_desc(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    if str(user.id) not in str(OWNER_ID):
        return msg.reply_text(
            "☞ Oɴʟʏ [owner_name](owner_tg) Hᴀᴠᴇ Pᴇʀᴍɪssɪᴏɴ ᴛᴏ Cʜᴀɴɢᴇ Tʜᴇ Sᴛɪᴄᴋᴇʀ Oғ Tʜᴇ Gʀᴏᴜᴘ"
        )

    tesc = msg.text.split(None, 1)
    if len(tesc) >= 2:
        desc = tesc[1]
    elif msg.reply_to_message:
        desc = msg.reply_to_message.text
    else:
        return msg.reply_text("» You want to set an empty Description 🤨!")

    try:
        if len(desc) > 255:
            return msg.reply_text(
                "☞ Description must be less than 255 words or characters !"
            )
        context.bot.set_chat_description(chat.id, desc)
        msg.reply_text(f"» Successfully updated chat description in {chat.title}!")
    except BadRequest as excp:
        msg.reply_text(f"Error ! {excp.message}.")



@bot_admin
@user_admin
def setchat_title(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    args = context.args
    if str(user.id) not in str(OWNER_ID):
        return msg.reply_text(
            "☞ Oɴʟʏ [owner_name](owner_tg) Hᴀᴠᴇ Pᴇʀᴍɪssɪᴏɴ ᴛᴏ Cʜᴀɴɢᴇ Tʜᴇ Sᴛɪᴄᴋᴇʀ Oғ Tʜᴇ Gʀᴏᴜᴘ"
        )
    title = " ".join(args)
    if not title:
        return msg.reply_text("» Enter Some Text To set it as New Chat Title !")
    try:
        context.bot.set_chat_title(int(chat.id), str(title))
        msg.reply_text(
            f"» Successfully set <b>{title}</b> as new chat title !",
            parse_mode=ParseMode.HTML,
        )
    except BadRequest as excp:
        return msg.reply_text(f"Error ! {excp.message}.")
        



@connection_status
@bot_admin # used to check bot is admin or not
@can_promote # used to check that bot have permission to promote or demote
@user_admin # Ths is used to check Owner id or Dev Id or Administrator
@loggable # used to send message in log chat 
def promote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    promoter = chat.get_member(user.id)
    if str(user.id) not in str(OWNER_ID):
        return message.reply_text("» Only @LegendBoy_OP have permission to promote anyone!")
    user_id = extract_user(message, args)
    if not user_id:
        return message.reply_text(
            "» I don't who is that never seen in any chat where i am present !",
        )
    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if user_member.status in ("administrator", "creator"):
        return message.reply_text("» According to me that user is already admin here !")
        

    if user_id == bot.id:
        return message.reply_text(
            "» Wtf ! How can i promote my self"
        )
        

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(bot.id)

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_change_info=bot_member.can_change_info,
            can_post_messages=bot_member.can_post_messages,
            can_edit_messages=bot_member.can_edit_messages,
            can_delete_messages=bot_member.can_delete_messages,
            can_invite_users=bot_member.can_invite_users,
            can_manage_voice_chats=bot_member.can_manage_voice_chats,
            can_pin_messages=bot_member.can_pin_messages,
        )
    except BadRequest as err:
        if err.message == "User_not_mutual_contact":
            message.reply_text("» According to me that user is not here.")
        else:
            message.reply_text(
                "» Something went wrong."
            )
        return

    bot.sendMessage(
        chat.id,
        f"<b>» Promoting a user in </b> {chat.title}\n\nPromoted : {mention_html(user_member.user.id, user_member.user.first_name)}\nPromoter : {mention_html(user.id, user.first_name)}",
        parse_mode=ParseMode.HTML,
    )

    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#ᴩʀᴏᴍᴏᴛᴇᴅ\n"
        f"<b>ᴩʀᴏᴍᴏᴛᴇʀ :</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>ᴜsᴇʀ :</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
    )
    return log_message



@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def lowpromote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    if str(user.id) not in str(DEV_USERS):
        return message.reply_text("» Dev Users & Owner have Only Permission to low Promote anyone!")
    user_id = extract_user(message, args)
    if not user_id:
        return message.reply_text(
            "» I don't who is that never seen in any chat where i am present !",
        )
    try:
        user_member = chat.get_member(user_id)
    except:
        return
    if user_member.status in ("administrator", "creator"):
        return message.reply_text("» According to me that user is already admin here !")
    if user_id == bot.id:
        return message.reply_text(
            "» Wtf ! How can i promote my self"
        )

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(bot.id)
    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_delete_messages=bot_member.can_delete_messages,
            can_invite_users=bot_member.can_invite_users,
            can_manage_voice_chats=bot_member.can_manage_voice_chats,
        )
    except BadRequest as err:
        if err.message == "User_not_mutual_contact":
            message.reply_text("» According to me that user is not here.")
        else:
            message.reply_text(
                "» Something went wrong."
            )
        return
    bot.sendMessage(
        chat.id,
        f"<b>» Promoting a user in </b>{chat.title}\n\n<b>Promoted :</b> {mention_html(user_member.user.id, user_member.user.first_name)}\n Promoter: {mention_html(user.id, user.first_name)}",
        
        parse_mode=ParseMode.HTML,
    )
    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#LowPromote\n"
        f"<b>ᴩʀᴏᴍᴏᴛᴇʀ :</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>ᴜsᴇʀ :</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
    )

    return log_message



@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def fullpromote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    promoter = chat.get_member(user.id)
    if str(user.id) not in str(OWNER_ID):
        return message.reply_text("➢ Owners have Only Permission to full Promote anyone!")
    user_id = extract_user(message, args)
    if not user_id:
        return message.reply_text(
            "» I don't who is that never seen in any chat where i am present !",
        )
    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if user_member.status in ("administrator", "creator"):
        return message.reply_text("» According to me that user is already admin here !")
    if user_id == bot.id:
        return message.reply_text(
            "» Wtf ! How can i promote my self"
        )

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(bot.id)
    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_change_info=bot_member.can_change_info,
            can_post_messages=bot_member.can_post_messages,
            can_edit_messages=bot_member.can_edit_messages,
            can_delete_messages=bot_member.can_delete_messages,
            can_invite_users=bot_member.can_invite_users,
            can_promote_members=bot_member.can_promote_members,
            can_restrict_members=bot_member.can_restrict_members,
            can_pin_messages=bot_member.can_pin_messages,
            can_manage_voice_chats=bot_member.can_manage_voice_chats,
        )
    except BadRequest as err:
        if err.message == "User_not_mutual_contact":
            message.reply_text("» According to me that user is not here.")
        else:
            message.reply_text(
                "» Something went wrong."
            )
        return
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "↻ Dᴇᴍᴏᴛᴇ ↺",
                    callback_data="demote_({})".format(user_member.user.id),
                )
            ]
        ]
    )
    bot.sendMessage(
        chat.id,
        f"» Successfully full promoted in <b>{chat.title}</b>\n\n<b>User : {mention_html(user_member.user.id, user_member.user.first_name)}</b>\n<b>Promoter : {mention_html(user.id, user.first_name)}</b>",
        parse_mode=ParseMode.HTML,
    )
    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#Fullpromoted\n"
        f"<b>Promoter :</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User :</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
    )
    return log_message



@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def demote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user
    if str(user.id) not in str(OWNER_ID):
        return message.reply_text("» Owners have Only Permission to Demote anyone!")
    user_id = extract_user(message, args)
    if not user_id:
        return message.reply_text(
            "» I don't who is that never seen in any chat where i am present !",
        )
    try:
        user_member = chat.get_member(user_id)
    except:
        return
    if user_member.status == "creator":
        return message.reply_text(
            "» Thats user is owner of this chat.I can't put myself in danger"
        )
  
    if not user_member.status == "administrator":
        message.reply_text("» According to me that user is not admin here !")
        return

    if user_id == bot.id:
        message.reply_text("» How can i demote myself 😳")
        return

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_voice_chats=False,
        )

        bot.sendMessage(
            chat.id,
            f"» Successfully demoted a admin in <b>{chat.title}</b>\n\nDemoted : <b>{mention_html(user_member.user.id, user_member.user.first_name)}</b>\nDemoter : {mention_html(user.id, user.first_name)}",
            parse_mode=ParseMode.HTML,
        )

        log_message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#Demoted\n"
            f"<b>Demoter :</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>Demoted :</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
        )

        return log_message
    except BadRequest:
        return message.reply_text("» Failed to demote Or may be someone promoted.")
       


@user_admin # check administrator owner & dev
@bot_admin
def refresh_admin(update, _):
    try:
        ADMIN_CACHE.pop(update.effective_chat.id)
    except KeyError:
        pass

    update.effective_message.reply_text("» Successfully refreshed admin cache !")



@connection_status
@bot_admin
@can_promote
@user_admin # check 3 people OWNER_ID ADMINSTRATOR & DEV USERS
def set_title(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user
    if str(user.id) not in str(DEV_USERS):
        return message.reply_text("Dev User & Owner Have Only Permission to change title")
    user_id, title = extract_user_and_text(message, args)
    try:
        user_member = chat.get_member(user_id)
    except:
        return
    if not user_id:
        message.reply_text(
            "» I don't who is that never seen in any chat where i am present !",
        )
        return
    if user_member.status == "creator":
        message.reply_text(
            "» That user is owner of the chat and i don't want to put myself in danger.",
        )
        return

    if user_member.status != "administrator":
        message.reply_text(
            "» I can only set title for admins !",
        )
        return

    if user_id == bot.id:
        message.reply_text(
            "» I can't set title for myself, My owner didn't told me to do so. ",
        )
        return

    if not title:
        message.reply_text(
            "» You think that setting blank title will change something 🧐?"
        )
        return

    if len(title) > 16:
        message.reply_text(
            "» Hadd h 🤨, The title length is longer than 16 word or character.",
        )
    try:
        bot.setChatAdministratorCustomTitle(chat.id, user_id, title)
    except BadRequest:
        message.reply_text(
            "» Maybe that user is not promoted by me or maybe you sent something that can't be set as title."
        )
        return

    bot.sendMessage(
        chat.id,
        f"» Successfully set title for <code>{user_member.user.first_name or user_id}</code> "
        f"To <code>{html.escape(title[:16])}</code>!",
        parse_mode=ParseMode.HTML,
    )



@bot_admin 
@can_pin #check that bot can promote admin or not
@user_admin #check that admin or dev or owner id
@loggable
def pin(update: Update, context: CallbackContext) -> str:
    bot, args = context.bot, context.args
    user = update.effective_user
    chat = update.effective_chat
    msg = update.effective_message
    msg_id = msg.reply_to_message.message_id if msg.reply_to_message else msg.message_id
    if str(user.id) not in str(DEV_USERS):
        return msg.reply_text("» Dev User & Owner have Only Permission to Pin any message!")
    if msg.chat.username:
        # If chat has a username, use this format
        link_chat_id = msg.chat.username
        message_link = f"https://t.me/{link_chat_id}/{msg_id}"
    elif (str(msg.chat.id)).startswith("-100"):
        # If chat does not have a username, use this
        link_chat_id = (str(msg.chat.id)).replace("-100", "")
        message_link = f"https://t.me/c/{link_chat_id}/{msg_id}"
    is_group = chat.type not in ("private", "channel")
    prev_message = update.effective_message.reply_to_message
    if prev_message is None:
        msg.reply_text("» Reply to a message to Pin it !")
        return
    is_silent = True
    if len(args) >= 1:
        is_silent = (
            args[0].lower() != "notify"
            or args[0].lower() == "loud"
            or args[0].lower() == "violent"
        )

    if prev_message and is_group:
        try:
            bot.pinChatMessage(
                chat.id, prev_message.message_id, disable_notification=is_silent
            )
            msg.reply_text(
                f"» Successfully pinned that message\n☞ Click on button below to see that message.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ᴍᴇssᴀɢᴇ", url=f"{message_link}")]]
                ),
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except BadRequest as excp:
            if excp.message != "Chat_not_modified":
                raise
        log_message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"Pinned a message\n"
            f"<b>Pinned by :</b> {mention_html(user.id, html.escape(user.first_name))}"
        )

        return log_message



@bot_admin
@can_pin #check that bot is admin or not
@user_admin #check that user is admin or not
@loggable
def unpin(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message
    msg_id = msg.reply_to_message.message_id if msg.reply_to_message else msg.message_id
    if str(user.id) not in str(OWNER_ID):
        return message.reply_text("» Owners have Only Permission to UnPin any message !") 
    if msg.chat.username:
        # If chat has a username, use this format
        link_chat_id = msg.chat.username
        message_link = f"https://t.me/{link_chat_id}/{msg_id}"
    elif (str(msg.chat.id)).startswith("-100"):
        # If chat does not have a username, use this
        link_chat_id = (str(msg.chat.id)).replace("-100", "")
        message_link = f"https://t.me/c/{link_chat_id}/{msg_id}"
    is_group = chat.type not in ("private", "channel")
    prev_message = update.effective_message.reply_to_message
    if prev_message and is_group:
        try:
            context.bot.unpinChatMessage(chat.id, prev_message.message_id)
            msg.reply_text(
                f"» Successfully unpinned <a href='{message_link}'> This pinned message</a>.",
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except BadRequest as excp:
            if excp.message != "Chat_not_modified":
                raise
    if not prev_message and is_group:
        try:
            context.bot.unpinChatMessage(chat.id)
            msg.reply_text("» Successfully unpinned last pinned message.")
        except BadRequest as excp:
            if excp.message == "Message to unpin not found":
                msg.reply_text(
                    "» I can't unpin that message, Maybe that message is too old or maybe someone already unpinned it."
                )
            else:
                raise

    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"Unpinned a message\n"
        f"<b>Unpinned by :</b> {mention_html(user.id, html.escape(user.first_name))}"
    )

    return log_message

@bot_admin
@can_pin
@user_admin
def unpinall(update: Update, context: CallbackContext):
    member = update.effective_chat.get_member(update.effective_user.id)
    if str(user.id) not in str(DEV_USERS):
        return update.effective_message.reply_text("➣ Owner & Dev User Have Only Permission to Used This Command")
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Are you sure you want to unpin all messages?",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(text="Yes", callback_data="unpinallbtn_yes"),
            InlineKeyboardButton(text="No", callback_data="unpinallbtn_no"),
        ]]),
    )

@bot_admin
@loggable
def unpinallbtn(update: Update, context: CallbackContext):
    bot = context.bot
    chat = update.effective_chat
    query = update.callback_query
    user = update.effective_user
    reply = query.data.split("_")[1]
    if str(user.id) not in str(DEV_USERS):
        return update.effective_message.reply_text("➣ Owner & Dev User Have Only Permission to Used This Command")
    if reply == 'yes':
        try:
            unpinned =  bot.unpinAllChatMessages(chat.id)
            if unpinned:
                query.message.edit_text("Successfully unpinned all messages!")
            else:
                query.message.edit_text("Failed to unpin all messages")
        except BadRequest as excp:
            if excp.message == "Chat_not_modified":
                pass
            else:
                raise
        
    else:
        query.message.edit_text("Unpin of all pinned messages has been cancelled.")
        return
    log_message = "<b>{}:</b>" \
                  "\n#UNPINNEDALL" \
                  "\n<b>Admin:</b> {}".format(
                      html.escape(chat.title),
                      mention_html(user.id, user.first_name),
                  )
    return log_message

@bot_admin
@user_admin # check dev user, owner & admin
@connection_status
def invite(update: Update, context: CallbackContext):
    bot = context.bot
    chat = update.effective_chat
    user = update.effective_user
    if str(user.id) not in str(DEV_USERS):
        return update.effective_message.reply_text("➣ Owner & Dev User Have Only Permission to Used This Command")
    
    if chat.username:
        update.effective_message.reply_text(f"https://t.me/{chat.username}")
    elif chat.type in [chat.SUPERGROUP, chat.CHANNEL]:
        bot_member = chat.get_member(bot.id)
        if bot_member.can_invite_users:
            invitelink = bot.exportChatInviteLink(chat.id)
            update.effective_message.reply_text(invitelink)
        else:
            update.effective_message.reply_text(
                "» I don't have permission to access invite chat links !",
            )
    else:
        update.effective_message.reply_text(
            "☞ I can only give invite links for group and channels !",
        )



@connection_status
def adminlist(update, context):
    chat = update.effective_chat  # type: Optional[Chat] -> unused variable
    user = update.effective_user  # type: Optional[User]
    args = context.args  # -> unused variable
    bot = context.bot
    if update.effective_message.chat.type == "private":
        send_message(
            update.effective_message,
            "» This command can only used in group not in pm.",
        )
        return
    update.effective_chat
    chat_id = update.effective_chat.id
    chat_name = update.effective_message.chat.title  # -> unused variable
    try:
        msg = update.effective_message.reply_text(
            "» Fetching admin list....",
            parse_mode=ParseMode.HTML,
        )
    except BadRequest:
        msg = update.effective_message.reply_text(
            "» Fetching admin list...",
            quote=False,
            parse_mode=ParseMode.HTML,
        )

    administrators = bot.getChatAdministrators(chat_id)
    text = "Admins in <b>{}</b>:".format(html.escape(update.effective_chat.title))
    for admin in administrators:
        user = admin.user
        status = admin.status
        custom_title = admin.custom_title

        if user.first_name == "":
            name = "☠ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛ"
        else:
            name = "{}".format(
                mention_html(
                    user.id,
                    html.escape(user.first_name + " " + (user.last_name or "")),
                ),
            )

        if user.is_bot:
            administrators.remove(admin)
            continue

        # if user.username:
        #    name = escape_markdown("@" + user.username)
        if status == "creator":
            text += "\n❖ Owner :"
            text += "\n<code> ➣ </code>{}\n".format(name)

            if custom_title:
                text += f"<code> ┗━ {html.escape(custom_title)}</code>\n"

    text += "\n✤ Admins :"

    custom_admin_list = {}
    normal_admin_list = []

    for admin in administrators:
        user = admin.user
        status = admin.status
        custom_title = admin.custom_title

        if user.first_name == "":
            name = "☠ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛ"
        else:
            name = "{}".format(
                mention_html(
                    user.id,
                    html.escape(user.first_name + " " + (user.last_name or "")),
                ),
            )
        # if user.username:
        #    name = escape_markdown("@" + user.username)
        if status == "administrator":
            if custom_title:
                try:
                    custom_admin_list[custom_title].append(name)
                except KeyError:
                    custom_admin_list.update({custom_title: [name]})
            else:
                normal_admin_list.append(name)

    for admin in normal_admin_list:
        text += "\n<code> ➙ </code>{}".format(admin)

    for admin_group in custom_admin_list.copy():
        if len(custom_admin_list[admin_group]) == 1:
            text += "\n<code> ➙ </code>{} | <code>{}</code>".format(
                custom_admin_list[admin_group][0],
                html.escape(admin_group),
            )
            custom_admin_list.pop(admin_group)

    text += "\n"
    for admin_group, value in custom_admin_list.items():
        text += "\n🔮 <code>{}</code>".format(admin_group)
        for admin in value:
            text += "\n<code> ➙ </code>{}".format(admin)
        text += "\n"

    try:
        msg.edit_text(text, parse_mode=ParseMode.HTML)
    except BadRequest:  # if original message is deleted
        return



@bot_admin
@can_promote
@user_admin
@loggable
def button(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    bot: Optional[Bot] = context.bot
    match = re.match(r"demote_\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        member = chat.get_member(user_id)
        bot_member = chat.get_member(bot.id)
        bot_permissions = promoteChatMember(
            chat.id,
            user_id,
            can_change_info=bot_member.can_change_info,
            can_post_messages=bot_member.can_post_messages,
            can_edit_messages=bot_member.can_edit_messages,
            can_delete_messages=bot_member.can_delete_messages,
            can_invite_users=bot_member.can_invite_users,
            can_promote_members=bot_member.can_promote_members,
            can_restrict_members=bot_member.can_restrict_members,
            can_pin_messages=bot_member.can_pin_messages,
            can_manage_voice_chats=bot_member.can_manage_voice_chats,
        )
        demoted = bot.promoteChatMember(
            chat.id,
            user_id,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_voice_chats=False,
        )
        if demoted:
            update.effective_message.edit_text(
                f"Demoter : {mention_html(user.id, user.first_name)}\nᴜsᴇʀ : {mention_html(member.user.id, member.user.first_name)}!",
                parse_mode=ParseMode.HTML,
            )
            query.answer("Demoted successfully !")
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#DEMOTE\n"
                f"<b>Demoter :</b> {mention_html(user.id, user.first_name)}\n"
                f"<b>User :</b> {mention_html(member.user.id, member.user.first_name)}"
            )
    else:
        update.effective_message.edit_text(
            "» Failed to demote, Maybe that user is not admin or maybe left the group !"
        )
        return ""


__help__ = """
✘ *User Commands*:
➣ /admins , /staff*:* list of admins in the chat

✘ *Dev User Commands:* 
➢ /pin*:* silently pins the message replied to - add `'loud'` or `'notify'` to give notifs to users
➢ /invitelink*:* gets invitelink
➢ /lowpromote*:* promotes the user replied to with half rights
➢ /title <title here>*:* sets a custom title for an admin that the bot promoted
➢ /admincache, /reload, /refresh *:* force refresh the admins list

✘ *Owner User Commands:*
➣ /promote*:* promotes the user replied to
➢ /unpin*:* unpins the currently pinned message
➢ /unpinall*:* unpin all the message
➣ /fullpromote*:* promotes the user replied to with full rights
➣ /demote*:* demotes the user replied to
➣ /setgtitle <text>*:* set group title
➣ /setgpic*:* reply to an image to set as group photo
➣ /setdesc*:* Set group description
➣ /setsticker*:* Set group sticker
➢ /delgpic *:* Delete Default Group Photo
"""

SET_DESC_HANDLER = CommandHandler("setdesc", set_desc)
SET_STICKER_HANDLER = CommandHandler("setsticker", set_sticker)
SETCHATPIC_HANDLER = CommandHandler("setgpic", setchatpic)
RMCHATPIC_HANDLER = CommandHandler("delgpic", rmchatpic)
SETCHAT_TITLE_HANDLER = CommandHandler("setgtitle", setchat_title)
ADMINLIST_HANDLER = DisableAbleCommandHandler(["admins", "staff"], adminlist)
PIN_HANDLER = CommandHandler("pin", pin)
UNPIN_HANDLER = CommandHandler("unpin", unpin)
UNPINALL_HANDLER = CommandHandler("unpinall", unpinall, filters=Filters.chat_type.groups, run_async=True)
UNPINALL_BTN_HANDLER = CallbackQueryHandler(unpinallbtn, pattern=r"unpinallbtn_")
INVITE_HANDLER = DisableAbleCommandHandler("invitelink", invite)
PROMOTE_HANDLER = DisableAbleCommandHandler("promote", promote)
FULLPROMOTE_HANDLER = DisableAbleCommandHandler("fullpromote", fullpromote)
LOW_PROMOTE_HANDLER = DisableAbleCommandHandler("lowpromote", lowpromote)
DEMOTE_HANDLER = DisableAbleCommandHandler("demote", demote)
SET_TITLE_HANDLER = CommandHandler("title", set_title)
ADMIN_REFRESH_HANDLER = CommandHandler(
    ["admincache", "reload", "refresh"],
    refresh_admin,
)
dispatcher.add_handler(SET_DESC_HANDLER)
dispatcher.add_handler(SET_STICKER_HANDLER)
dispatcher.add_handler(SETCHATPIC_HANDLER)
dispatcher.add_handler(RMCHATPIC_HANDLER)
dispatcher.add_handler(SETCHAT_TITLE_HANDLER)
dispatcher.add_handler(ADMINLIST_HANDLER)
dispatcher.add_handler(PIN_HANDLER)
dispatcher.add_handler(UNPIN_HANDLER)
dispatcher.add_handler(UNPINALL_HANDLER)
dispatcher.add_handler(UNPINALL_BTN_HANDLER)
dispatcher.add_handler(INVITE_HANDLER)
dispatcher.add_handler(PROMOTE_HANDLER)
dispatcher.add_handler(FULLPROMOTE_HANDLER)
dispatcher.add_handler(LOW_PROMOTE_HANDLER)
dispatcher.add_handler(DEMOTE_HANDLER)
dispatcher.add_handler(SET_TITLE_HANDLER)
dispatcher.add_handler(ADMIN_REFRESH_HANDLER)

__mod_name__ = "Admins"
__command_list__ = [
    "setdesc" "setsticker" "setgpic" "delgpic" "setgtitle" "title" "adminlist",
    "admins",
    "invitelink",
    "promote",
    "fullpromote",
    "lowpromote",
    "demote",
    "admincache",
    "unpinall",
]
__handlers__ = [
    SET_DESC_HANDLER,
    SET_STICKER_HANDLER,
    SETCHATPIC_HANDLER,
    RMCHATPIC_HANDLER,
    SETCHAT_TITLE_HANDLER,
    ADMINLIST_HANDLER,
    PIN_HANDLER,
    UNPIN_HANDLER,
    UNPINALL_HANDLER,
    INVITE_HANDLER,
    PROMOTE_HANDLER,
    FULLPROMOTE_HANDLER,
    LOW_PROMOTE_HANDLER,
    DEMOTE_HANDLER,
    SET_TITLE_HANDLER,
    ADMIN_REFRESH_HANDLER,
]
