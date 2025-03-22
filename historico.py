from transacao import Transacao
from datetime import datetime, timezone

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
                'Data': datetime.now(timezone.utc).strftime('%d/%m/%Y - %H:%M:%S')
            }
        )
        
    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or tipo_transacao == transacao['Tipo']:
                yield transacao
                
    def transacoes_do_dia(self):
        data_atual = datetime.now(timezone.utc).strftime('%d/%m/%Y')
        transacoes = []
        for transacao in self._transacoes:
            data_itens = transacao['Data'].split(' ')
            data_transacao = data_itens[0]
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes