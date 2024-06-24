import streamlit as st
from tiny_llama_gguf import TinyLlama
from chat_history_db import ChatHistoryDB
from const.pre_prompts import PrePrompts
class StreamlitApp:
    def __init__(self) -> None:
        self._initialize_streamlit_app()
        self._load_model()
        self._initialize_db()
        self._initialize_sidbar_button()

        # Initialize Chat id
        if 'chat_id' not in st.session_state:
            st.session_state.chat_id = None

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

    def _default_welcome_message(self):
        # Add initial message by the user
        user_initial_message = "Hello Assistant!"
        st.session_state['chat_history_db'].add_message_to_db(st.session_state['chat_id'], "user", user_initial_message)

    def _initialize_sidbar_button(self):
        # Create new session button
        if st.sidebar.button("New Chat!"):
            st.session_state['chat_history_db'].create_new_chat()
        

    def get_selected_chat_history(self):
        # Initialize chat history from the selected session
        return st.session_state['chat_history_db'].get_chat_history_from_chat_id(st.session_state.chat_id)
    
    def get_last_user_message(self):
        history = self.get_selected_chat_history()[-1]
        last_user_message = [data['content'] for data in [history] if data['role'] == 'user'][-1]
        return last_user_message
    
    def display_messages_from_history(self, chat_history):
        for message in chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def display_instant_message(self, role, message):
        # Add user message to chat history
        st.session_state['chat_history_db'].add_message_to_db(st.session_state['chat_id'], role, message)
        # Instance displaying user message in chat message container
        with st.chat_message(role):
            message_placeholder = st.empty()
            message_placeholder.markdown(message)

    def generate_response(self, chat_history):
        response = st.session_state['tinyllama'].generate_response(chat_history)
        return response
    
    def model_response(self, chat_history):
        response = self.generate_response(chat_history)
        return response

    def run(self):
        st.session_state['chat_history_db'].display_chats()

        # Display welcome message if no chat session is active
        if not st.session_state.chat_id:
            st.write("Welcome! Please create a new chat or select an existing one from the sidebar.")
        
        elif st.session_state.chat_id:
            chat_history = self.get_selected_chat_history()
            if chat_history:
                self.display_messages_from_history(chat_history)         

            user_message = st.chat_input("Write your message...") 
            if user_message:
                self.display_instant_message("user", user_message)
                chat_history = self.get_selected_chat_history()
                response = self.model_response(chat_history)
                self.display_instant_message("assistant", response)

    
if __name__ == '__main__':
    StreamlitApp().run()