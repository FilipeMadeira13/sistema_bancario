from conta import Conta
from transacao import Transacao


class Deposito(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor

    def registrar(self, conta) -> None:
        registro_autorizado = conta.depositar(self._valor)

        if registro_autorizado:
            conta._historico.adicionar_transacao(self)
