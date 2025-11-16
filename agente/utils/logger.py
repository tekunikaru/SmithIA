import logging

class log:
    def __init__(self, nome:str,arquivo="smith.log",nivel=logging.INFO,elevar_em_erro=False):
        self.nome = nome
        self.elevar = elevar_em_erro
        logging.basicConfig(filename=arquivo, level=nivel)
    
    def _formatar(self,mensagem)->str:
        mensagem = f'{self.nome}:{mensagem}'
        print(mensagem)
        return mensagem

    def aviso(self, mensagem):
        logging.warning(self._formatar(mensagem))
        
    def info(self, mensagem):
        logging.info(self._formatar(mensagem))

    def erro(self, mensagem):
        logging.error(self._formatar(mensagem))
        if self.elevar:
            raise RuntimeError(mensagem)
