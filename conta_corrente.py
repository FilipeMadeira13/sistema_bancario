from conta import Conta
from saque import Saque


class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente, limite=500, limite_saques=3) -> None:
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        numero_saques = len(
            [
                transacao
                for transacao in self._historico._transacoes
                if transacao["Tipo"] == Saque.__name__
            ]
        )

        if numero_saques >= self._limite_saques:
            print("Limite de saques atingido! Tente novamente amanhã.")
        elif valor > self._limite:
            print(
                f"Só é permitido no máximo o valor de R$ {self._limite:.2f} a cada saque."
            )
        else:
            return super().sacar(valor)

        return False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self._agencia}, {self._numero}, {self._cliente.nome}>"

    def __str__(self) -> str:
        return f"""
            Agencia:\t{self._agencia}
            Número da conta:\t{self._numero}
            Cliente:\t{self._cliente.nome}
    """
