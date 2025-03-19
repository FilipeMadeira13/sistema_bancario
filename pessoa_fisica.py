from cliente import Cliente

class PessoaFisica(Cliente):
    def __init__(self, endereco: str, cpf: str, nome: str, data_nascimento) -> None:
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento