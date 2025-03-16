from transacao import Transacao

class Saque(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor