import streamlit as st
import time
from tinydb import TinyDB, Query

class ChatHistoryDB:
    def __init__(self, db_name) -> None:
        self._initialize_db(db_name)

    def _initialize_db(self, db_name):
        self.db = TinyDB(f'{db_name}.json')
        self.session = Query()
        print('db loaded')

    def create_new_chat(self):
        new_chat_id = f"chat_{int(time.time())}"
        self.db.insert({"chat_id": new_chat_id, "messages": []})
        st.session_state.chat_id = new_chat_id
        st.experimental_rerun()

    def get_chat_history_from_chat_id(self, chat_id):
        session = self.db.get(self.session.chat_id == chat_id)
        return session['messages'] if session else []
    
    def add_message_to_db(self, chat_id, role, content):
        session = self.db.get(self.session.chat_id == chat_id)
        if session:
            session['messages'].append({"role": role, "content": content})
            self.db.update(session, self.session.chat_id == chat_id)

    def delete_chat_history_from_chat_id(self, chat_id):
        self.db.remove(self.session.chat_id == chat_id)

    # Display session buttons
    def display_chats(self):
        sessions = self.db.all()
        for session in sessions:
            chat_id = session['chat_id']
            if st.sidebar.button(chat_id, use_container_width=True):
                st.session_state.chat_id = chat_id
                st.experimental_rerun()