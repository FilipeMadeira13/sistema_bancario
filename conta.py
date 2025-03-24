from historico import Historico


class Conta:
    def __init__(self, numero: int, cliente) -> None:
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero: int):
        return cls(numero, cliente)

    def sacar(self, valor: float) -> bool:
        if valor > self._saldo:
            print(
                f"Saldo insuficiente! Tente sacar um valor de no máximo R$ {self._saldo:.2f}"
            )
        elif valor > 0:
            self._saldo -= valor
            print(f"Saque de R$ {valor:.2f} efetuado com sucesso.")
            return True
        else:
            print("Erro! Valor inválido.")

        return False

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("Por favor, digite apenas números positivos.")
            return False

        self._saldo += valor
        print(f"Deposito de R$ {valor:.2f} efetuado com sucesso.")
        return True

    def __str__(self) -> str:
        return (
            f"Agencia: {self._agencia}\n"
            f"Número da Conta: {self._numero}\n"
            f"Cliente: {self._cliente}\n"
            f"Saldo: {self._saldo:.2f}"
        )
