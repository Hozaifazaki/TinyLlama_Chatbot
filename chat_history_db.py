import streamlit as st
import time
from tinydb import TinyDB, Query

class ChatHistoryDB:
    def __init__(self, db_name) -> None:
        self._initialize_db(db_name)
        self.chat_id = None
    def _initialize_db(self, db_name):
        self.db = TinyDB(f'{db_name}.json')
        self.session = Query()
        
    def set_chat_id(self, chat_id):
        self.chat_id = chat_id

    def get_chat_id(self):
        return self.chat_id

    def create_new_chat(self):
        new_chat_id = f"chat_{int(time.time())}"
        self.db.insert({"chat_id": new_chat_id, "messages": []})
        self.set_chat_id(new_chat_id)

    def get_chat_history_from_chat_id(self):
        session = self.db.get(self.session.chat_id == self.chat_id)
        return session['messages'] if session else []
    
    def add_message_to_db(self, role, content):
        session = self.db.get(self.session.chat_id == self.chat_id)
        if session:
            session['messages'].append({"role": role, "content": content})
            self.db.update(session, self.session.chat_id == self.chat_id)

    def delete_chat_history_from_chat_id(self):
        self.db.remove(self.session.chat_id == self.chat_id)

    def get_all_chats(self):
        return self.db.all()