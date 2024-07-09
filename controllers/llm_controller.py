from models.tiny_llama_gguf import TinyLlama
from models.phi3_mini_gguf import PhiMini

class LLMController:
    def __init__(self, gen_args, model_name='TinyLlama-1.1B', model_path=None) -> None:
        """
        Initialize the LLMController with generation arguments and model path.
        """
        if model_name == 'Phi-3-mini':
            self.llm_model = PhiMini(gen_args, model_path)
            print('phi')
        else:
            self.llm_model = TinyLlama(gen_args, model_path)
            print('tiny')

        self.model_name = model_name
        self.load_model()

    def set_chat_history(self, chat_history=None):
        """
        Set the chat history in the model.
        """
        self.llm_model.set_chat_history(chat_history)

    def set_system_message(self, system_message=None):
        """
        Set the system message in the model.
        """
        self.llm_model.set_system_message(system_message)

    def load_model(self):
        """
        Load the model.
        """
        self.llm_model.load_model()
        self.llm_model.connect_to_wikipedia_tool()
        self.llm_model.initialize_llm_agent()

    def generate_response(self, chat_history=None):
        """
        Generate a response based on the chat history.
        """
        self.set_chat_history(chat_history)
        memory = self.llm_model.create_prompt_template()
        return self.llm_model.generate_response(memory)

    def get_generated_response(self):
        """
        Get the generated response from the model.
        """
        return self.llm_model.get_generated_response()
