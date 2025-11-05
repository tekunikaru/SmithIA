import logging

class log:
    def __init__(self, nome):
        self.nome = nome
        logging.basicConfig(filename="claudio.log", level=logging.INFO)
    
    def warning(self, message):
        logging.warning(f'{self.nome}:{message}')
        print(message)
        
    def info(self, message):
        logging.info(f'{self.nome}:{message}', )
        print(message)

    def error(self, message):
        logging.error(f'{self.nome}:{message}')
        raise RuntimeError(message)
