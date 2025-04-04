"""
Sistema de Produtos

Este sistema permite criar, listar, atualizar e deletar produtos de um banco de dados local SQLite.
Ele é útil para controlar o estoque de produtos de forma simples via terminal.

Funcionalidades:
- Inserir novo produto
- Listar todos os produtos
- Atualizar quantidade e preço
- Deletar produto por ID
- Validações e tratamento de erros

Gabriel Gonçalves Sá
Matricula: 22352853
"""

import sqlite3
from typing import Optional

MAX_INT_SQLITE = 9223372036854775807
MIN_INT_SQLITE = 0

def executar_sql(query: str, params=(), fetch: bool = False):
    """Executa comandos SQL com ou sem retorno."""
    try:
        with sqlite3.connect('estoque.db') as conexao:
            cursor = conexao.cursor()
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            conexao.commit()
            return cursor
    except sqlite3.DatabaseError as e:
        print(f"Erro no banco de dados: {e}")
        return None

def criar_banco_de_dados():
    """Cria a tabela de produtos se ela não existir."""
    executar_sql('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    ''')

def criar_produto(nome: str, quantidade: int, preco: float):
    """Adiciona um novo produto ao banco."""
    if not nome.strip():
        print("Erro: Nome do produto não pode estar vazio.")
        return
    if not (MIN_INT_SQLITE <= quantidade <= MAX_INT_SQLITE):
        print("Erro: Quantidade fora do limite permitido.")
        return
    if preco < 0:
        print("Erro: O preço deve ser um valor positivo.")
        return

    try:
        executar_sql('''
            INSERT INTO produtos (nome, quantidade, preco)
            VALUES (?, ?, ?)
        ''', (nome, quantidade, preco))
        print("Produto inserido com sucesso.")
    except sqlite3.IntegrityError:
        print(f"Erro: O produto '{nome}' já existe.")

def listar_produtos():
    """Exibe todos os produtos cadastrados."""
    produtos = executar_sql("SELECT * FROM produtos", fetch=True)
    if produtos:
        print("Produtos disponíveis no estoque:")
        for produto in produtos:
            print(f"ID: {produto[0]} | Nome: {produto[1]} | Quantidade: {produto[2]} | Preço: R${produto[3]:.2f}")
    else:
        print("Não há produtos cadastrados.")

def atualizar_produto(id_produto: int, nova_quantidade: int, novo_preco: float):
    """Atualiza um produto existente com novos dados."""
    if not (MIN_INT_SQLITE <= id_produto <= MAX_INT_SQLITE):
        print("Erro: ID inválido.")
        return
    if not (MIN_INT_SQLITE <= nova_quantidade <= MAX_INT_SQLITE):
        print("Erro: Quantidade fora do limite permitido.")
        return
    if novo_preco < 0:
        print("Erro: O preço deve ser positivo.")
        return

    produto = executar_sql("SELECT * FROM produtos WHERE id = ?", (id_produto,), fetch=True)
    if produto:
        executar_sql("""
            UPDATE produtos SET quantidade = ?, preco = ? WHERE id = ?
        """, (nova_quantidade, novo_preco, id_produto))
        print("Produto atualizado com sucesso.")
    else:
        print("Erro: Produto não encontrado.")

def deletar_produto(id_produto: int):
    """Remove um produto pelo ID."""
    if not (MIN_INT_SQLITE <= id_produto <= MAX_INT_SQLITE):
        print("Erro: ID fora do limite permitido.")
        return

    cursor = executar_sql("DELETE FROM produtos WHERE id = ?", (id_produto,))
    if cursor and cursor.rowcount > 0:
        print("Produto deletado com sucesso.")
    else:
        print("Erro: Produto não encontrado.")

def ler_int(mensagem: str) -> Optional[int]:
    """Lê um número inteiro do usuário."""
    try:
        return int(input(mensagem))
    except ValueError:
        print("Erro: Digite um número inteiro válido.")
        return None

def ler_float(mensagem: str) -> Optional[float]:
    """Lê um número decimal do usuário."""
    try:
        return float(input(mensagem).replace(",", "."))
    except ValueError:
        print("Erro: Digite um número válido.")
        return None

def criar_produto_interativo():
    """Lê os dados do produto e chama a criação."""
    nome = input("Digite o nome do produto: ")
    quantidade = ler_int("Digite a quantidade do produto: ")
    preco = ler_float("Digite o preço do produto: ")
    if quantidade is not None and preco is not None:
        criar_produto(nome, quantidade, preco)

def atualizar_produto_interativo():
    """Lê os dados do produto e chama a atualização."""
    id_produto = ler_int("Digite o ID do produto a ser atualizado: ")
    nova_quantidade = ler_int("Digite a nova quantidade do produto: ")
    novo_preco = ler_float("Digite o novo preço do produto: ")
    if id_produto is not None and nova_quantidade is not None and novo_preco is not None:
        atualizar_produto(id_produto, nova_quantidade, novo_preco)

def deletar_produto_interativo():
    """Lê o ID do produto e chama a exclusão."""
    id_produto = ler_int("Digite o ID do produto a ser deletado: ")
    if id_produto is not None:
        deletar_produto(id_produto)

def exibir_menu():
    """Exibe o menu principal e executa a ação escolhida."""
    acoes = {
        '1': criar_produto_interativo,
        '2': listar_produtos,
        '3': atualizar_produto_interativo,
        '4': deletar_produto_interativo,
        '5': lambda: exit()
    }

    while True:
        print("\nMenu:")
        print("1. Criar novo produto")
        print("2. Listar todos os produtos")
        print("3. Atualizar produto")
        print("4. Deletar produto")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")
        acao = acoes.get(opcao)
        if acao:
            acao()
        else:
            print("Opção inválida. Tente novamente.")

def main():
    """Inicializa o banco e inicia o menu."""
    try:
        criar_banco_de_dados()
        exibir_menu()
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")

if __name__ == "__main__":
    main()
