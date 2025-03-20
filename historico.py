from transacao import Transacao
from datetime import datetime

class Historico:
    def __init__(self) -> None:
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao) -> None:
        self._transacoes.append(
            {
                'Tipo': transacao.__class__.__name__,
                'Valor': transacao._valor,
                'Data': datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
            }
        )
        
    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao == 'd':
                if transacao['Tipo'] == 'Deposito':
                    yield transacao
            elif tipo_transacao == 's':
                if transacao['Tipo'] == 'Saque':
                    yield transacao
            else:
                yield transacao