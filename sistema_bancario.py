menu = '''
======== BEM-VINDO AO SISTEMA BANCÁRIO ========
    Escolha uma opção abaixo:
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair: 
'''

saldo = 0
limite = 500
extrato = ''
numero_saques = 0
LIMITE_SAQUES = 3


while True:
    opcao = input(menu).strip().lower()
    try:
        if opcao == 'd':
            deposito = float(input('Digite o valor do depósito: '))
            
            if deposito <= 0:
                print('Por favor, digite apenas números positivos.')
                continue
            
            saldo += deposito
            print(f'Deposito de R$ {deposito:.2f} efetuado com sucesso.')
            extrato += f'DEPÓSITO.........R$ {deposito:.2f}\n'
            
        elif opcao == 's':
            if numero_saques >= LIMITE_SAQUES:
                print('Limite de saques atingido! Tente novamente amanha.')
                continue
            
            saque = float(input(f'Digite o valor do saque (MAX: R$ {limite:.2f}): '))
            
            if saque <= 0:
                print('Por favor, digite apenas números positivos.')
                continue
            
            if saque > limite:
                print(f'Só é permitido no máximo o valor de R$ {limite:.2f} a cada saque.')
                continue
            
            if saque > saldo:
                print(f'Saldo insuficiente! Tente sacar um valor de no máximo R$ {saldo:.2f}')
                continue
                
            saldo -= saque
            numero_saques += 1
            print(f'Saque de R$ {saque:.2f} efetuado com sucesso.')
            extrato += f'SAQUE.............R$ {saque:.2f}\n'
            
        elif opcao == 'e':
            if not extrato:
                print('Não houve movimentações no extrato hoje.')
            
            print('========== EXTRATO ==========')
            print(extrato + f'\n\nSALDO ATUAL.......R$ {saldo:.2f}')
                
            
        elif opcao == 'q':
            print('Obrigado por usar nosso sistema! Tenha um bom dia!😊')
            break
        else:
            print('Por favor digite apenas uma opção válida.')
            
    except ValueError:
        print('Valor inválido! Por favor, digite apenas números.')