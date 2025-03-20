from cliente import Cliente
from conta import Conta
from conta_corrente import ContaCorrente
from deposito import Deposito
from historico import Historico
from pessoa_fisica import PessoaFisica
from saque import Saque
from transacao import Transacao
from conta_iterador import ContaIterador
from datetime import datetime
import re
import functools

agora = datetime.now()

def menu():
    menu = '''
    ======== BEM-VINDO AO SISTEMA BANCÁRIO ========
        Escolha uma opção abaixo:   
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [u]\tCadastrar Cliente
    [c]\tCadastrar Conta Corrente
    [l]\tListar Clientes
    [t]\tListar Contas
    [q]\tSair: 
    '''
    return input(menu).strip().lower()

def log_transacao(func):
    @functools.wraps(func)
    def opcao(*args, **kwargs):
        print(f'Tipo: {opcao.__name__.title()}')
        resultado = func(*args, **kwargs)
        print(f'Data e Hora: {agora.strftime("%d/%m/%Y %H:%M:%S")}')
        return resultado
        
    return opcao

@log_transacao
def cadastrar_cliente(clientes: list):
    cpf = input('Digite o CPF do cliente (somente números): ').strip()
    
    cpf_valido = validar_cpf(cpf)
    
    if not cpf_valido:
        return
    
    cliente = encontrar_cliente(cpf, clientes)
    
    if cliente:
        print('Cliente com este CPF já existe.')
        return
    
    nome = input('Digite o nome completo: ').title().strip()
    
    if not nome:
        print('O campo com o nome não pode ficar vazio')
        return
    
    data_nascimento = input('Data de nascimento (DD/MM/AAAA): ').strip()
    data_valida = validar_data(data_nascimento)
    
    if not data_valida:
        return
    
    print('Digite abaixo as informações de endereço:\n')
    logradouro = input('Rua: ').title().strip()
    numero_da_moradia = input('Número da moradia: ').strip()
    bairro = input('Bairro: ').title().strip()
    cidade = input('Cidade: ').title().strip()
    sigla_estado = input('Estado (sigla): ').upper().strip()
    
    if len(sigla_estado) != 2:
        print('Estado inválido! Digite apenas a sigla.')
        return
                    
    endereco = f'{logradouro}, {numero_da_moradia} - {bairro} - {cidade}/{sigla_estado}'
    
    cliente = PessoaFisica(endereco, cpf, nome, data_nascimento)
    
    clientes.append(cliente)
    
    print('Cliente cadastrado com sucesso!')

@log_transacao    
def criar_conta(numero_conta: int, clientes: list, contas: list):
    cpf = input('Digite o CPF do cliente (somente números): ').strip()
    
    cliente = encontrar_cliente(cpf, clientes)
    
    if not cliente:
        print('Cliente não encontrado')
        return None
    
    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente._contas.append(conta)
    
    print('Conta criada com sucesso!')

@log_transacao  
def depositar(clientes: list):
    cpf = input('Digite o CPF do cliente (somente números): ').strip()
    
    cliente = encontrar_cliente(cpf, clientes)
    
    if not cliente:
        print('Cliente não encontrado')
        return None
    
    conta = procurar_conta_cliente(cliente)
    
    if not conta:
        return
    
    if len(conta._historico.transacoes) >= 10:
        print('Limite de transações diárias atingido. Tente novamente amanhã.')
        return
    
    valor = float(input(f'Digite o valor do depósito: '))
    transacao = Deposito(valor)
    
    cliente.realizar_transacao(conta, transacao)
    
def encontrar_cliente(cpf: str, clientes: list):
    cliente_encontrado = [cliente for cliente in clientes if cliente._cpf == cpf]
    
    return cliente_encontrado[0] if cliente_encontrado else None

@log_transacao
def exibir_extrato(clientes: list):
    cpf = input('Digite o CPF do cliente (somente números): ').strip()
    
    cliente = encontrar_cliente(cpf, clientes)
    
    if not cliente:
        print('Cliente não encontrado')
        return None
    
    conta = procurar_conta_cliente(cliente)
    
    if not conta:
        return
    
    
    transacoes = conta._historico.transacoes
    
    extrato = ''
    if not transacoes:
        extrato = 'Não existem transações na conta.'
    else:
        tipo_transacao = input('Digite a letra correspondente se deseja ver apenas as transações relacionada a "[s] Saque" ou "[d] Depósito" (ou qualquer outra para ver todos): ').strip().lower()
    
        print('=============== EXTRATO ===============\n')
        for transacao in conta._historico.gerar_relatorio(tipo_transacao):
            extrato += f'\n{transacao["Tipo"]}.......................R$ {transacao["Valor"]:.2f}'
            
    print(extrato)
    print(f'\nSaldo.......................R$ {conta.saldo:.2f}')
    print('========================================\n')

def listar_clientes(clientes: list):
    if not clientes:
        print('Não existem clientes cadastrados.')
        return
    
    print('=============== Clientes ===============\n')
    for cliente in clientes:
        print(f" - {cliente._nome} / Data de Nascimento: {cliente._data_nascimento} / CPF: {cliente._cpf} / Endereço: {cliente._endereco}")

def listar_contas(contas: list):
    print('============ Contas Corrente ============\n')
    for conta in ContaIterador(contas):
        print(conta)
        print("-" * 40)

def procurar_conta_cliente(cliente):
    if not cliente._contas:
        print('Cliente não possui contas.')
        return
    
    numero = int(input('Escolha a conta pelo número (ex: primeira, digite "1"): '))
    
    if numero > len(cliente._contas) or numero <= 0:
        print('Essa não é uma conta válida.')
        return
    
    return cliente._contas[numero - 1]

@log_transacao
def sacar(clientes: list):
    cpf = input('Digite o CPF do cliente (somente números): ').strip()
    
    cliente = encontrar_cliente(cpf, clientes)
    
    if not cliente:
        print('Cliente não encontrado')
        return None
    
    conta = procurar_conta_cliente(cliente)
    
    if not conta:
        return
    
    if len(conta._historico.transacoes) >= 10:
        print('Limite de transações diárias atingido para essa conta. Tente novamente amanhã.')
        return
    
    valor = float(input(f'Digite o valor do saque: '))
    transacao = Saque(valor)
    
    cliente.realizar_transacao(conta, transacao)

def validar_cpf(cpf: str):
    padrao_cpf = r'\d{11}'
                    
    if not re.match(padrao_cpf, cpf):
        print('CPF Inválido!')
        return False
    
    return True
                 
def validar_data(data: str):
    padrao_data = r'\d{2}/\d{2}/\d{4}'
                    
    if not re.match(padrao_data, data):
        print('Formato de data inválido!')
        return False
    
    return True

def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()
        
        try:
            if opcao == 'd':
                depositar(clientes)
            elif opcao == 's':
                sacar(clientes)
            elif opcao == 'e':
                exibir_extrato(clientes)
            elif opcao == 'u':
                cadastrar_cliente(clientes)
            elif opcao == 'c':
                numero_conta = len(contas) + 1
                criar_conta(numero_conta, clientes, contas)
            elif opcao == 'l':
                listar_clientes(clientes)   
            elif opcao == 't':
                listar_contas(contas)
            elif opcao == 'q':
                print('Obrigado por usar nosso sistema! Tenha um bom dia!😊')
                break
            else:
                print('Por favor digite apenas uma opção válida.')
                
        except ValueError:
            print('Valor inválido! Por favor, digite apenas números.')

if __name__ == '__main__':
    main()