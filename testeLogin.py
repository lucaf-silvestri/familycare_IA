import hashlib
import sqlite3

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('familycare.db')
cursor = conn.cursor()

def criptografar_senha(senha):
    return hashlib.md5(senha.encode()).hexdigest()

def login_idoso(conn, nome, senha):
    cursor = conn.cursor()
    senha_hash = criptografar_senha(senha)  # Criptografa a senha fornecida
    cursor.execute('''
        SELECT * FROM Idosos WHERE nome = ? AND senha = ?
    ''', (nome, senha_hash))
    
    idoso = cursor.fetchone()
    if idoso:
        print("Login bem-sucedido.")
        return True
    else:
        print("Nome ou senha incorretos.")
        return False
    
def login_cuidador(conn, nome, senha):
    cursor = conn.cursor()
    senha_hash = criptografar_senha(senha)  # Criptografa a senha fornecida
    cursor.execute('''
        SELECT * FROM Cuidadores WHERE nome = ? AND senha = ?
    ''', (nome, senha_hash))
    
    idoso = cursor.fetchone()
    if idoso:
        print("Login bem-sucedido.")
        return True
    else:
        print("Nome ou senha incorretos.")
        return False
    
escolha = int(input("\nEscolha o tipo de usuário que deseja realizar login: \n1 - Idoso\n2 - Cuidador\n"))

if escolha == 1:
    nome = input("\nInforme seu nome: ")
    senha = input("Informe sua senha: ")
    login_idoso(conn, nome, senha)
elif escolha == 2:
    nome = input("\nInforme seu nome: ")
    senha = input("Informe sua senha: ")
    login_cuidador(conn, nome, senha)
else:
    print("Você não escolheu uma opção válida.\n")
