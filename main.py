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
from pathlib import Path
import re
import functools
import os

# Constantes
ROOT_PATH = Path(__file__).parent
REGISTROS = ROOT_PATH / 'registros'
ARQUIVO_LOG = REGISTROS / 'log.txt'
ARQUIVO_CLIENTES = REGISTROS / 'clientes.txt'
ARQUIVO_CONTAS = REGISTROS / 'contas.txt'

# Variáveis
agora = datetime.now()

def menu():
    menu = '''
    ======== BEM-VINDO AO SISTEMA BANCÁRIO ========
    *ATENÇÃO: MÁXIMO DE 10 TRANSAÇÕES DIÀRIAS POR CONTA*
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
        data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
        tipo = opcao.__name__.title()
        print(f'Tipo: {tipo}')
        resultado = func(*args, **kwargs)
        
        # Registros de log
        try:
            if not REGISTROS.exists():
                os.mkdir(REGISTROS)
            with open(ARQUIVO_LOG, 'a', encoding='utf-8') as arquivo:
                arquivo.write(f' - Data e Hora: {data_hora}\t- Tipo: {tipo}\n - Registros: {args if args else ""}{f" {kwargs}" if kwargs else ""}\t- Resultado: {"Nenhum Retorno" if not resultado else resultado}\n{"-" * 80}\n')
        except IOError as e:
            print(f'Erro ao criar o arquivo: {e}')
            return
        except Exception as e:
            print(f'Erro desconhecido: {e}')
            return
        
        print(f'Data e Hora: {data_hora}')
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
    
    try:
        if not REGISTROS.exists():
            os.mkdir(REGISTROS)
        with open(ARQUIVO_CLIENTES, 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'{cliente}\n')
    except IOError as e:
        print(f'Erro ao criar o arquivo: {e}')
        return
    except Exception as e:
        print(f'Erro desconhecido: {e}')
        return
    
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
    cliente.contas.append(conta)
    
    try:
        if not REGISTROS.exists():
            os.mkdir(REGISTROS)
        with open(ARQUIVO_CONTAS, 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'{conta}\n')
    except IOError as e:
        print(f'Erro ao criar o arquivo: {e}')
        return
    except Exception as e:
        print(f'Erro desconhecido: {e}')
        return
    
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
    
    
    transacoes = conta.historico.transacoes
    
    extrato = ''
    if not transacoes:
        extrato = 'Não existem transações na conta.'
    else:
        tipo_transacao_input = input('Digite a letra correspondente se deseja ver apenas as transações relacionada a "[s] Saque" ou "[d] Depósito" (ou qualquer outra para ver todos): ').strip().lower()
    
        tipo_transacao = 'Saque' if tipo_transacao_input == 's' else 'Deposito' if tipo_transacao_input == 'd' else None
        print('=============== EXTRATO ===============\n')
        for transacao in conta.historico.gerar_relatorio(tipo_transacao):
            extrato += f'\n{transacao["Data"]}\n{transacao["Tipo"]}.......................R$ {transacao["Valor"]:.2f}\n'
            
    print(extrato)
    print(f'\nSaldo.......................R$ {conta.saldo:.2f}')
    print('========================================\n')

def listar_clientes(clientes: list):
    if not clientes:
        print('Não existem clientes cadastrados.')
        return
    
    print('=============== Clientes ===============\n')
    for cliente in clientes:
        print(f" - {cliente.nome} / Data de Nascimento: {cliente.data_nascimento} / CPF: {cliente.cpf} / Endereço: {cliente.endereco}")

def listar_contas(contas: list):
    print('============ Contas Corrente ============\n')
    for conta in ContaIterador(contas):
        print(conta)
        print("-" * 40)

def procurar_conta_cliente(cliente):
    if not cliente.contas:
        print('Cliente não possui contas.')
        return
    
    numero = int(input('Escolha a conta pelo número (ex: primeira, digite "1"): '))
    
    if numero > len(cliente.contas) or numero <= 0:
        print('Essa não é uma conta válida.')
        return
    
    return cliente.contas[numero - 1]

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
                
        except ValueError as e:
            print(f'Valor inválido! Por favor, digite apenas números: {e}')

if __name__ == '__main__':
    main()