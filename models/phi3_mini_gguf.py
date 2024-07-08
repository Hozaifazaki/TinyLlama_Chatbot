from const.app_paths import AppPaths
from langchain_community.llms import LlamaCpp

class PhiMini:
    def __init__(self, gen_args, model_path=None) -> None:
        """
        Initialize the Phi3 Mini model with generation arguments and model path.
        """
        self.gen_args = gen_args
        self.model_path = model_path if model_path else AppPaths.PHI_MINI_MODEL_PATH
        self.system_message = ''
        self.chat_history = None
        self.generated_response = ''
        self.llm = None

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
        system_token = "<|system|>"
        user_token = "<|user|>"
        assistant_token = "<|assistant|>"
        end_token = "<|end|>"

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

    def generate_response(self, memory=None):
        """
        Generate response based on the provided memory.
        """
        self.generated_response = ''
        for token in self.llm.stream(memory):
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
