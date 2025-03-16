from conta import Conta
from transacao import Transacao

class Cliente:
    def __init__(self, endereco: str, contas: list) -> None:
        self._endereco = endereco
        self._contas = contas
        
    def realizar_transacao(self, conta: Conta, transacao: Transacao) -> None:
        pass
    
    def adicionar_conta(self, conta: Conta) -> None:
        pass