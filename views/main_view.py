import streamlit as st

class MainView:
    def __init__(self) -> None:
        self._initialize_main_view()
        pass

    def _initialize_main_view(self):
        # Set app title
        st.title("TinyLlama Chatbot")

    def display_welcome_message():
        st.write("Welcome! Please create a new chat or select an existing one from the sidebar.")
