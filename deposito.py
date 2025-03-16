from transacao import Transacao

class Deposito(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor