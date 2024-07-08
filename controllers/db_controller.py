from core.controller import Controller
from models.chat_history_db import ChatHistoryDB


class DBController(Controller):
    def __init__(self):
        self.db = ChatHistoryDB()
    
    def set_chat_id(self, chat_id):
        self.db.set_chat_id(chat_id)

    def get_chat_id(self):
        return self.db.get_chat_id()

    def create_new_chat(self):
        self.db.create_new_chat()

    def get_chat_history_from_chat_id(self):
        self.db.get_chat_history_from_chat_id()

    def get_all_chats(self):
        self.db.get_all_chats()

    def add_message_to_db(self, role, content):
        self.add_message_to_db(role, content)

    def delete_chat_history_from_chat_id(self):
        self.db.delete_chat_history_from_chat_id()
