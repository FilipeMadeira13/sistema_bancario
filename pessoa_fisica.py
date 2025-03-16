from cliente import Cliente
from datetime import date

class PessoaFisica(Cliente):
    def __init__(self, endereco: str, contas: list, cpf: str, nome: str, data_nascimento: date) -> None:
        super().__init__(endereco, contas)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento