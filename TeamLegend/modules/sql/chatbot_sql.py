import threading

from sqlalchemy import Column, String

from TeamLegend.modules.sql import BASE, SESSION


class KannadigaChats(BASE):
    __tablename__ = "kannadiga_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


KannadigaChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_kannadiga(chat_id):
    try:
        chat = SESSION.query(KannadigaChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()


def set_kannadiga(chat_id):
    with INSERTION_LOCK:
        fallenchat = SESSION.query(KannadigaChats).get(str(chat_id))
        if not fallenchat:
            kannadigachat = KannadigaChats(str(chat_id))
        SESSION.add(fallenchat)
        SESSION.commit()


def rem_kannadiga(chat_id):
    with INSERTION_LOCK:
        fallenchat = SESSION.query(KannadigaChats).get(str(chat_id))
        if kannadigachat:
            SESSION.delete(kannadigachat)
        SESSION.commit()
