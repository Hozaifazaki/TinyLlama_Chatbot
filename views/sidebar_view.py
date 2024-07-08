import streamlit as st
from controllers.db_controller import DBController

class SideBar:
    def __init__(self) -> None:
        self.controller = DBController()
        
    def _initialize_sidebar(self):
        # Sidebar for session management
        st.sidebar.title("Chat History")
    
    def _initialize_sidbar_button(self):
        # Create new session button
        if st.sidebar.button("New Chat!", use_container_width=True):
            self.controller.create_new_chat()
            st.session_state['chat_id'] = self.controller.get_chat_id()
            st.rerun()
        
        if st.sidebar.button("Clear Chat", use_container_width=True):
            self.controller.delete_chat_history_from_chat_id()
            st.session_state['chat_id'] = None
            st.rerun()

    # Display session buttons
    def display_history_on_sidebar(self):
        sessions = self.controller.get_all_chats()
        for session in sessions:
            chat_id = session['chat_id']
            if st.sidebar.button(chat_id, use_container_width=True):
                st.session_state['chat_id'] = chat_id
                # set chat id on chat history button clicked
                self.controller.set_chat_id(st.session_state['chat_id'])
                st.rerun()  

    def show(self):
        self._initialize_sidebar()
        self._initialize_sidbar_button()
        self.display_history_on_sidebar()
    
if __name__ == '__main__':
    SideBar()
