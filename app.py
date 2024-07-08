import streamlit as st
from models.chat_history_db import ChatHistoryDB
from const.pre_prompts import PrePrompts
from controllers.llm_controller import LLMController
import time

@st.cache_resource
def load_model():
    pass 


class StreamlitApp:
    def __init__(self) -> None:
        self._initialize_streamlit_app()
        self._initialize_db()
        self._initialize_sidbar()
        self._initialize_streamlit_states()

    def _initialize_streamlit_app(self):
        st.title("Chatbot")
    
    def _initialize_streamlit_states(self):
        # Initialize Chat id
        if 'chat_id' not in st.session_state:
            st.session_state['chat_id'] = None
        
        # Initialize selected model
        if 'selected_model' not in st.session_state:
            st.session_state['selected_model'] = None
            
    def _load_model(self):
        if "llm_model" not in st.session_state or st.session_state['llm_model'].model_name != st.session_state['selected_model']:
            st.session_state["llm_model"] = LLMController({
                'temperature': 0.8,
                'max_length': 512,
                'top_p': 1 
            },
            model_name=st.session_state['selected_model']
            )
        
        system_message = PrePrompts.system_prompt 
        st.session_state['llm_model'].set_system_message(system_message)


    def _initialize_db(self):
        if "chat_history_db" not in st.session_state:
            st.session_state['chat_history_db'] = ChatHistoryDB()

    def _initialize_sidbar(self):
        # Sidebar for session management
        st.sidebar.header("Chat Configurations")
        # Create new session button
        if st.sidebar.button("New Chat", use_container_width=True):
            st.session_state['chat_history_db'].create_new_chat()
            st.session_state['chat_id'] = st.session_state['chat_history_db'].get_chat_id()
            st.rerun()
        
        if st.sidebar.button("Clear Chat", use_container_width=True):
            st.session_state['chat_history_db'].delete_chat_history_from_chat_id()
            st.session_state['chat_id'] = None
            st.rerun()
        
        st.sidebar.header("Select Model")
        self.model_selection_button()



    # Display session buttons
    def display_history_on_sidebar(self):
        sessions = st.session_state['chat_history_db'].get_all_chats()
        st.sidebar.header("Chat History")
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
        return st.session_state['llm_model'].generate_response(chat_history)

    def save_message(self, role, message):
        st.session_state['chat_history_db'].add_message_to_db(role, message)
    
    def model_selection_button(self):
        # Define the label and list of options for the radio buttons
        models = ["TinyLlama-1.1B", "Phi-3-mini"]

        # Create the radio button widget and store the selected option
        selected_model = st.sidebar.radio(label='', label_visibility='collapsed', options=models, index=None)

        if selected_model:
            st.session_state['selected_model'] = models[0] if selected_model == models[0] else models[1]

    def run(self):
        self.display_history_on_sidebar()
        
        # Display welcome message if no chat session is active
        if not st.session_state['chat_id']:
            st.success("Welcome! Please create a new chat or select an existing one from the sidebar.")
        
        else:
            chat_history = self.get_selected_chat_history()
            if bool(chat_history):
                self.display_messages_from_history(chat_history)         


            if not st.session_state.get('selected_model'):
                st.warning("Please select a model before sending a message.")
            
            user_message = st.chat_input("Write your message...") 

            if user_message:
                self.display_instant_message("user", user_message)
                self.save_message('user', user_message)

                chat_history = self.get_selected_chat_history()

                if st.session_state['selected_model']:
                    with st.spinner("Loading model..."):
                        self._load_model()
                    
                    with st.spinner("Generating Response..."):
                        time.sleep(1)
                        response = self.generate_response(chat_history)
                        self.display_instant_message("assistant", response)
                    self.save_message("assistant", st.session_state['llm_model'].get_generated_response())

if __name__ == '__main__':
    StreamlitApp().run()