from const.app_paths import AppPaths
from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate


class TinyLlama:
    def __init__(self, gen_args, model_path=None) -> None:
        self.gen_args = gen_args
        self.model_path = model_path if model_path else AppPaths.MODEL_PATH
        self.llm = self.load_model()
        self.system_message = ''
        self.chat_history = None
        # self.memory = self.create_chat_memory()
        self.memory = ''
    
    def set_chat_history(self, chat_history=None):
        self.chat_history = chat_history

    def set_system_message(self, system_message=None):
        self.system_message = system_message

    def create_prompt_template(self):
        self.memory = ''
        system_token = "<|system|>"
        user_token = "<|user|>"
        assistant_token = "<|assistant|>"
        end_token = "</s>"

        self.memory += f"{system_token}\n{self.system_message}{end_token}\n"

        for message in self.chat_history:  
            role = message['role']
            content = message['content']
            if role == "user":
                self.memory += f"{user_token}\n{content}{end_token}\n"
            else:
                self.memory += f"{assistant_token}\n{content}{end_token}\n"
        
        self.memory += f"{assistant_token}\n"
        print('\n\n')
        print('################## Previous chat ###############')
        print(self.memory)
        print('\n\n')
        
    def load_model(self):
        # Make sure the model path is correct for your system!
        llm = LlamaCpp(
            model_path=self.model_path,
            temperature=self.gen_args['temprature'],
            max_tokens=self.gen_args['max_length'],
            top_p=self.gen_args['top_p'],
            verbose=True,  # Verbose is required to pass to the callback manager
        )
        return llm

    def generate_response(self, chat_history):
        self.set_chat_history(chat_history)
        self.create_prompt_template()
        response = self.llm.invoke(self.memory)
        return response

    def parse_output(self):
        pass
