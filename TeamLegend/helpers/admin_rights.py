from telegram import Chat, User
from TeamLegend.Config import OWNER_ID


def user_can_promote(chat: Chat, user: User, bot_id: int) -> bool:
    return chat.get_member(user.id).can_promote_members


def user_can_ban(chat: Chat, user: User, bot_id: int) -> bool:
    return chat.get_member(user.id).can_restrict_members


def user_can_pin(chat: Chat, user: User, bot_id: int) -> bool:
    return chat.get_member(user.id).can_pin_messages

#This is used to Check right of Change Info of OWNER_ID
def user_can_changeinfo(chat: Chat, user: User, bot_id: int) -> bool:
    return chat.get_member(OWNER_ID).can_change_info
