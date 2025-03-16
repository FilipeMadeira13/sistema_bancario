from cliente import Cliente
from historico import Historico

class Conta:
    def __init__(self, saldo: float, numero: int, agencia: str, cliente: Cliente, historico: Historico) -> None:
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = historico
        
    def saldo(self):
        pass
    
    def nova_conta(self, cliente: Cliente, historico: Historico):
        pass
    
    def sacar(self, valor: float):
        pass
    
    def depositar(self, valor: float):
        pass
