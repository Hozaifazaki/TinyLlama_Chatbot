import abc

class Controller(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def execute_command(self):
        return
    
    @abc.abstractmethod
    def take_command(self):
        return
    
    @abc.abstractmethod
    def main(self):
        return
    