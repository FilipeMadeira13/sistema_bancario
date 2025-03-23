from conta_corrente import ContaCorrente


class ContaIterador:
    def __init__(self, contas) -> None:
        self._contas = contas
        self._contador = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self._contas[self._contador]
            self._contador += 1
            return str(conta)
        except IndexError:
            if self._contador == 0:
                print("Não existem contas cadastradas.")

            raise StopIteration
