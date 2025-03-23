from conta import Conta
from transacao import Transacao


class Cliente:
    def __init__(self, endereco: str) -> None:
        self._endereco = endereco
        self._contas = []

    @property
    def contas(self):
        return self._contas

    @property
    def endereco(self):
        return self._endereco

    def realizar_transacao(self, conta, transacao) -> None:
        if len(conta._historico.transacoes_do_dia()) >= 10:
            print("Limite de transações diárias atingido. Tente novamente amanhã.")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta) -> None:
        self._contas.append(conta)
