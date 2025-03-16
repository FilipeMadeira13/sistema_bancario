from conta import Conta
from cliente import Cliente
from historico import Historico

class ContaCorrente(Conta):
    def __init__(self, saldo: float, numero: int, agencia: str, cliente: Cliente, historico: Historico, limite: float, limite_saques: int) -> None:
        super().__init__(saldo, numero, agencia, cliente, historico)
        self._limite = limite
        self._limite_saques = limite_saques