import time
from tinydb import TinyDB, Query
from const.app_paths import AppPaths

class ChatHistoryDB:
    def __init__(self) -> None:
        self._initialize_db()
        self.chat_id = None

    def _initialize_db(self):
        self.db = TinyDB(f'{AppPaths.DB_PATH}')
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
    
    def get_all_chats(self):
        return self.db.all()
    
    def add_message_to_db(self, role, content):
        session = self.db.get(self.session.chat_id == self.chat_id)
        if session:
            session['messages'].append({"role": role, "content": content})
            self.db.update(session, self.session.chat_id == self.chat_id)

    def delete_chat_history_from_chat_id(self):
        self.db.remove(self.session.chat_id == self.chat_id)

