from const.app_paths import AppPaths
from langchain_community.llms import LlamaCpp
from const.model_special_tokens import SpecialTokens
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks.streamlit.streamlit_callback_handler import StreamlitCallbackHandler
import streamlit as st
class TinyLlama:
    def __init__(self, gen_args, model_path=None) -> None:
        """
        Initialize the TinyLlama model with generation arguments and model path.
        """
        self.gen_args = gen_args
        self.model_path = model_path if model_path else AppPaths.TINY_LLAMA_MODEL_PATH
        self.system_message = ''
        self.chat_history = None
        self.generated_response = ''
        self.llm = None
        self.agent_tools = []

    def set_chat_history(self, chat_history=None):
        """
        Set the chat history.
        """
        self.chat_history = chat_history

    def set_system_message(self, system_message=None):
        """
        Set the system message.
        """
        self.system_message = system_message

    def create_prompt_template(self):
        """
        Create the prompt template based on system message and chat history.
        """
    def create_prompt_template(self):
        memory = ''
        system_token = SpecialTokens.TINY_LLAMA['system_token']
        user_token = SpecialTokens.TINY_LLAMA['user_token']
        assistant_token = SpecialTokens.TINY_LLAMA['assistant_token']
        end_token = SpecialTokens.TINY_LLAMA['end_token']

        memory += f"{system_token}\n{self.system_message}{end_token}\n"

        for message in self.chat_history:
            role = message['role']
            content = message['content']
            if role == "user":
                memory += f"{user_token}\n{content}{end_token}\n"
            else:
                memory += f"{assistant_token}\n{content}{end_token}\n"

        memory += f"{assistant_token}\n"
        print('\n\n')
        print('################## Previous chat ###############')
        print(memory)
        print('\n\n')
        return memory

    def load_model(self):
        """
        Load the LlamaCpp model.
        """
        self.llm = LlamaCpp(
            model_path=self.model_path,
            temperature=self.gen_args['temperature'],
            max_tokens=self.gen_args['max_length'],
            top_p=self.gen_args['top_p'],
            n_ctx=4000,
            verbose=False,
        )
    
    def connect_to_wikipedia_tool(self):
        api_wrapper = WikipediaAPIWrapper(
            top_k_results= 3,
            doc_content_chars_max= 500
        )

        wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
        self.agent_tools.append(wiki_tool)

        return wiki_tool

    def initialize_llm_agent(self):
        self.agent = initialize_agent(
            agent="zero-shot-react-description",
            tools=self.agent_tools,
            llm=self.llm,
            verbose=False,
            # max_iterations=3,
            handle_parsing_errors=True,
        )


    def generate_response(self, memory=None):
        """
        Generate response based on the provided memory.
        """
        st_callback = StreamlitCallbackHandler(
            st.container(),
            expand_new_thoughts=False,
            max_thought_containers=2,
            )

        self.generated_response = ''
        for token in self.agent.run(memory, callbacks=[st_callback]):
            yield token
            self.generated_response += token

    def get_generated_response(self):
        """
        Get the generated response.
        """
        return self.generated_response

    def parse_output(self):
        """
        Parse the output if needed.
        """
        pass
