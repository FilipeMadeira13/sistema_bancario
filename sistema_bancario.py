menu = '''
======== BEM-VINDO AO SISTEMA BANCÁRIO ========
    Escolha uma opção abaixo:
    
[d] Depositar
[s] Sacar
[e] Extrato
[u] Cadastrar Usuário
[c] Cadastrar Conta Corrente
[l] Listar Usuários
[t] Listar Contas
[q] Sair: 
'''

lista_de_usuarios = []
contas = []


def sacar(*, saldo: float, valor: float, extrato: str, limite: float, numero_saques: int, limite_saques: int):
    if numero_saques >= limite_saques:
        print('Limite de saques atingido! Tente novamente amanha.') 
    elif valor <= 0:
        print('Por favor, digite apenas números positivos.')   
    elif valor > limite:
        print(f'Só é permitido no máximo o valor de R$ {limite:.2f} a cada saque.')
    elif valor > saldo:
        print(f'Saldo insuficiente! Tente sacar um valor de no máximo R$ {saldo:.2f}')
    else:            
        saldo -= valor
        numero_saques += 1
        print(f'Saque de R$ {valor:.2f} efetuado com sucesso.')
        extrato += f'SAQUE.............R$ {valor:.2f}\n'
    
    return saldo, extrato, numero_saques
    
def depositar(saldo: float, valor: float, extrato: str, /):
    if valor <= 0:
        print('Por favor, digite apenas números positivos.')
    else:            
        saldo += valor
        print(f'Deposito de R$ {valor:.2f} efetuado com sucesso.')
        extrato += f'DEPÓSITO.........R$ {valor:.2f}\n'
    
    return saldo, extrato
    
def visualizar_extrato(saldo: float, /, *, extrato: str):
    if not extrato:
        print('Não houve movimentações no extrato hoje.')
                
    print('========== EXTRATO ==========')
    print(extrato + f'\n\nSALDO ATUAL.......R$ {saldo:.2f}')
    print('=============================') 
    
def cadastrar_usuario(nome: str, data_de_nascimento: str, cpf: str, endereco: str):
    for usuario in lista_de_usuarios:
        if cpf == usuario['CPF']:
            print('O CPF a ser cadastrado já existe.')
            return
        
    usuario = {
        'Nome': nome,
        'Data de Nascimento': data_de_nascimento,
        'CPF': cpf,
        'Endereço': endereco
    }
    print(usuario)
    lista_de_usuarios.append(usuario)
    
def cadastrar_conta_corrente(agencia: str, numero_da_conta: int, usuario: dict):
    conta_corrente = {
        'Agência': agencia,
        'Número da Conta': numero_da_conta,
        'Usuário': usuario['Nome']
    }
    contas.append(conta_corrente)
    
def listar_usuarios():
    if not lista_de_usuarios:
        print('Não existem usuários cadastrados.')
        return
    
    print('========== Usuários ==========\n')
    for usuario in lista_de_usuarios:
        print(f" - {usuario['Nome']} / Data de Nascimento: {usuario['Data de Nascimento']} / CPF: {usuario['CPF']} / Endereço: {usuario['Endereço']}")
    
def listar_contas():
    if not contas:
        print('Não existem contas cadastradas.')
        return
    
    print('========== Contas Corrente ==========\n')
    for conta in contas:
        print(f" {conta['Número da Conta']} - {conta['Usuário']}")

def main():
    # Variáveis
    saldo = 0
    limite = 500
    extrato = ''
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = '0001'
    numero_da_conta = 0

    while True:
        opcao = input(menu).strip().lower()
        try:
            if opcao == 'd':
                valor = float(input('Digite o valor do depósito: '))
                saldo, extrato = depositar(saldo, valor, extrato)
                
            elif opcao == 's':
                valor = float(input(f'Digite o valor do saque (MAX: R$ {limite:.2f}): '))
                
                saldo, extrato, numero_saques = sacar(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
                
            elif opcao == 'e':
                visualizar_extrato(saldo, extrato=extrato)
                
            elif opcao == 'u':
                while True:
                    nome = input('\nDigite o nome do usuário para cadastrá-lo: ').title().strip()
                    
                    if not nome:
                        print('O campo de nome não pode ficar vazio.')
                        continue
                    
                    data_de_nascimento = input('Data de nascimento (DD/MM/AAAA): ').strip()
                    numeros_data = data_de_nascimento.replace('/', '')
                    
                    if (not '/' in data_de_nascimento) or (len(data_de_nascimento) != 10) or (not numeros_data.isdigit()):
                        print('Formato de data inválido!')
                        continue
                    
                    cpf = input('CPF (Apenas números): ').strip()
                    
                    if (len(cpf) != 11) or (not cpf.isdigit()):
                        print('CPF Inválido!')
                        continue
                    
                    print('Digite abaixo as informações de endereço:\n')
                    logradouro = input('Rua: ').title().strip()
                    numero_da_moradia = input('Número da moradia: ').strip()
                    bairro = input('Bairro: ').title().strip()
                    cidade = input('Cidade: ').title().strip()
                    sigla_estado = input('Estado (sigla): ').upper().strip()
                    
                    if len(sigla_estado) != 2:
                        print('Estado inválido! Digite apenas a sigla.')
                        continue
                    
                    endereco = f'{logradouro}, {numero_da_moradia} - {bairro} - {cidade}/{sigla_estado}'
                    
                    cadastrar_usuario(nome, data_de_nascimento, cpf, endereco)
                    print('Usuário cadastrado com sucesso.')
                    break
                
            elif opcao == 'c':
                usuario_cpf = input('Digite o CPF do usuário a ter a conta cadastrada (somente números): ').strip()
                
                for usuario in lista_de_usuarios:
                    if usuario_cpf == usuario['CPF']:
                        numero_da_conta += 1
                        cadastrar_conta_corrente(AGENCIA, numero_da_conta, usuario)
                        print('Conta cadastrada com sucesso.')
                        break
                else:
                    print('Usuário não encontrado.')
                    
            elif opcao == 'l':
                listar_usuarios()
                
            elif opcao == 't':
                listar_contas()
                
            elif opcao == 'q':
                print('Obrigado por usar nosso sistema! Tenha um bom dia!😊')
                break
            else:
                print('Por favor digite apenas uma opção válida.')
                
        except ValueError:
            print('Valor inválido! Por favor, digite apenas números.')
            
if __name__ == '__main__':
    main()