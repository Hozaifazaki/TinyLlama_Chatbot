import streamlit as st
from tiny_llama_gguf import TinyLlama
from models.chat_history_db import ChatHistoryDB
from const.pre_prompts import PrePrompts


class StreamlitApp:
    def __init__(self) -> None:
        self._initialize_streamlit_app()
        self._load_model()
        self._initialize_db()
        self._initialize_sidbar_button()

        # Initialize Chat id
        if 'chat_id' not in st.session_state:
            st.session_state['chat_id'] = None

    def _initialize_streamlit_app(self):
        st.title("TinyLlama Chatbot")
        # Sidebar for session management
        st.sidebar.title("Chat History")

    def _load_model(self):
        if "tinyllama" not in st.session_state:
            st.session_state["tinyllama"] = TinyLlama({
                'temprature': 0.8,
                'max_length': 512,
                'top_p': 1 
            })
            system_message = PrePrompts.system_prompt 
            st.session_state['tinyllama'].set_system_message(system_message)

    def _initialize_db(self):
        if "chat_history_db" not in st.session_state:
            st.session_state['chat_history_db'] = ChatHistoryDB('chat_history_db')

    def _initialize_sidbar_button(self):
        # Create new session button
        if st.sidebar.button("New Chat!", use_container_width=True):
            st.session_state['chat_history_db'].create_new_chat()
            st.session_state['chat_id'] = st.session_state['chat_history_db'].get_chat_id()
            st.rerun()
        
        if st.sidebar.button("Clear Chat", use_container_width=True):
            st.session_state['chat_history_db'].delete_chat_history_from_chat_id()
            st.session_state['chat_id'] = None
            st.rerun()

    # Display session buttons
    def display_history_on_sidebar(self):
        sessions = st.session_state['chat_history_db'].get_all_chats()
        for session in sessions:
            chat_id = session['chat_id']
            if st.sidebar.button(chat_id, use_container_width=True):
                st.session_state['chat_id'] = chat_id
                # set chat id on chat history button clicked
                st.session_state['chat_history_db'].set_chat_id(st.session_state['chat_id'])
                st.rerun()    

    def get_selected_chat_history(self):
        # Initialize chat history from the selected session
        return st.session_state['chat_history_db'].get_chat_history_from_chat_id()
    
    def display_messages_from_history(self, chat_history):
        for message in chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def display_instant_message(self, role, message):
        # Instance displaying user message in chat message container
        with st.chat_message(role):
            if role == "assistant":
                st.write_stream(message)
            else:
                st.markdown(message)
    
    def generate_response(self, chat_history):
        response = st.session_state['tinyllama'].generate_response(chat_history)
        return response

    def save_message(self, role, message):
        st.session_state['chat_history_db'].add_message_to_db(role, message)

    def run(self):
        self.display_history_on_sidebar()
        
        # Display welcome message if no chat session is active
        if not st.session_state['chat_id']:
            st.write("Welcome! Please create a new chat or select an existing one from the sidebar.")
        
        else:
            chat_history = self.get_selected_chat_history()
            if chat_history:
                self.display_messages_from_history(chat_history)         

            user_message = st.chat_input("Write your message...") 
            if user_message:
                self.display_instant_message("user", user_message)
                self.save_message('user', user_message)

                chat_history = self.get_selected_chat_history()

                response = self.generate_response(chat_history)
                self.display_instant_message("assistant", response)
                # Add Assistant message to chat history
                self.save_message("assistant", st.session_state['tinyllama'].get_generated_response())

    
if __name__ == '__main__':
    StreamlitApp().run()