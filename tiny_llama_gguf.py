from const.app_paths import AppPaths
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class TinyLlama:
    def __init__(self, gen_args, model_path=None) -> None:
        self.gen_args = gen_args
        self.model_path = model_path if model_path else AppPaths.MODEL_PATH
        self.llm = self.load_model()
        self.system_message = ''
        self.chat_history = None
        self.memory = ''
        self.generated_reponse = ''
    
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
            n_ctx=2048,
            verbose=False,
        )
        print('Tinyllama loaded')
        return llm

    def generate_response(self, chat_history):
        self.set_chat_history(chat_history)
        self.create_prompt_template()
        
        self.generated_reponse = ''
        for token in self.llm.stream(self.memory):
             yield token
             self.generated_reponse += token

    def get_generated_response(self):
        return self.generated_reponse
    
    def parse_output(self):
        pass
