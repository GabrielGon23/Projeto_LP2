# Sistema de Gerenciamento de Estoque

Este projeto é um sistema de produtos desenvolvido em Python, utilizando um banco de dados SQLite local. 
Ele implementa funções Crud de cadastro, visualização, atualização e remoção de produtos por meio de uma interface interativa no terminal.

## Funcionalidades

- Inserir novo produto
- Listar todos os produtos cadastrados
- Atualizar a quantidade e o preço de um produto
- Deletar produto por ID
- Validação de entrada e tratamento de erros

## Como Executar

1. Certifique-se de que você tem o Python 3 instalado.
2. Execute o arquivo:

```bash
python main.py
```

3. Siga as instruções no terminal.

## Estrutura do Banco de Dados

O banco `estoque.db` será criado automaticamente ao executar o programa, com a seguinte estrutura:

```sql
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL
);
```

## Testes Realizados

### Funcionais:

- Cadastro de produtos válidos
- Listagem de produtos
- Atualização de quantidade e preço de produtos existentes
- Remoção de produtos por ID

### Validação e erros:

- Tentativa de inserir produto com nome vazio
- Inserção com quantidade negativa ou fora do limite
- Inserção de preço negativo
- Produto com nome duplicado
- Atualizar produto inexistente
- Digitar letras onde se espera número (ID, quantidade, preço)
- Atualizar com valores fora dos limites do SQLite (overflow)
- Interrupção do programa via `CTRL+C` (tratado com KeyboardInterrupt)

## Autor

Gabriel Gonçalves Sá  
Matrícula: 22352853
