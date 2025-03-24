# Sistema Bancário

## Descrição
Este é um Sistema Bancário desenvolvido como parte do desafio da DIO. O sistema implementa funcionalidades básicas de um banco, permitindo operações como depósito, saque, extrato, cadastro de clientes e contas.

## Versão
Versão 3.5

## Funcionalidades
- Cadastro de clientes (pessoa física)
- Criação de contas correntes
- Depósito
- Saque (com limite diário)
- Extrato (com filtros por tipo de transação)
- Listagem de clientes
- Listagem de contas
- Log de transações

## Regras de Negócio
- Limite de 10 transações diárias por conta
- Limite de 3 saques diários por conta corrente
- Limite de R$ 500,00 por saque
- Persistência de dados em arquivos de texto

## Tecnologias Utilizadas
- Python 3.x
- Programação Orientada a Objetos
- Design Patterns (Iterator, Template Method)
- Manipulação de arquivos
- Decoradores

## Como Executar
1. Certifique-se de ter o Python 3.x instalado
2. Clone o repositório: `git clone https://github.com/FilipeMadeira13/sistema_bancario.git`
3. Navegue até o diretório do projeto: `cd sistema-bancario`
4. Execute o arquivo principal: `python main.py`

## Fluxo de Uso
1. Execute o programa
2. Cadastre um cliente (`u`)
3. Crie uma conta corrente para o cliente (`c`)
4. Realize operações como depósito (`d`), saque (`s`) ou consulta de extrato (`e`)
5. Liste clientes (`l`) ou contas (`t`) quando necessário
6. Para sair do sistema, digite `q`

## Melhorias Futuras
- Implementar autenticação de usuários
- Adicionar transferências entre contas
- Implementar outros tipos de contas (poupança, investimento)
- Desenvolver interface gráfica
- Migrar para um banco de dados relacional

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias.


## Autor
Filipe Madeira

## Agradecimentos
- Digital Innovation One (DIO) pelo desafio proposto