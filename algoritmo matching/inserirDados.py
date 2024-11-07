import sqlite3
from faker import Faker
import random

# Configurando Faker para gerar dados fictícios
fake = Faker("pt_BR")

# Conectando ao banco de dados
conn = sqlite3.connect('familycare.db')
cursor = conn.cursor()

# Criação das tabelas (Idosos e Cuidadores)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Idosos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        idade INTEGER,
        sexo TEXT,
        contato TEXT,
        endereco TEXT,
        mobilidade TEXT,
        obesidade TEXT,
        deficiencia TEXT,
        dificuldadesVisuais TEXT,
        dificuldadesAuditivas TEXT,
        usoMedicamentos TEXT,
        alimentacaoAssistida TEXT,
        higieneAssistida TEXT,
        alergias TEXT,
        condicaoMedica TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cuidadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        idade INTEGER,
        sexo TEXT,
        contato TEXT,
        endereco TEXT,
        mobilidade TEXT,
        obesidade TEXT,
        deficiencia TEXT,
        dificuldadesVisuais TEXT,
        dificuldadesAuditivas TEXT,
        condicaoMedica TEXT
    )
''')

# Função para inserir idosos aleatórios
def inserir_idosos_aleatorios(n=10):
    for _ in range(n):
        nome = fake.name()
        idade = random.randint(65, 95)
        sexo = random.choice(["Masculino", "Feminino"])
        contato = fake.phone_number()
        endereco = fake.address()
        mobilidade = random.choice(["Sim", "Não"])
        obesidade = random.choice(["Sim", "Não"])
        deficiencia = random.choice(["Sim", "Não"])
        dificuldadesVisuais = random.choice(["Sim", "Não"])
        dificuldadesAuditivas = random.choice(["Sim", "Não"])
        usoMedicamentos = random.choice(["Sim", "Não"])
        alimentacaoAssistida = random.choice(["Sim", "Não"])
        higieneAssistida = random.choice(["Sim", "Não"])
        alergias = random.choice(["Sim", "Não"])
        condicaoMedica = random.choice(["Sim", "Não"])  # Alterado para "Sim" ou "Não"
        
        cursor.execute('''INSERT INTO Idosos (
                            nome, idade, sexo, contato, endereco, mobilidade, obesidade, deficiencia,
                            dificuldadesVisuais, dificuldadesAuditivas, usoMedicamentos, alimentacaoAssistida, 
                            higieneAssistida, alergias, condicaoMedica)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (nome, idade, sexo, contato, endereco, mobilidade, obesidade, deficiencia, 
                        dificuldadesVisuais, dificuldadesAuditivas, usoMedicamentos, alimentacaoAssistida, 
                        higieneAssistida, alergias, condicaoMedica))
    conn.commit()
    print(f"{n} idosos inseridos com sucesso.")

# Função para inserir cuidadores aleatórios
def inserir_cuidadores_aleatorios(n=10):
    for _ in range(n):
        nome = fake.name()
        idade = random.randint(25, 60)
        sexo = random.choice(["Masculino", "Feminino"])
        contato = fake.phone_number()
        endereco = fake.address()
        mobilidade = random.choice(["Sim", "Não"])
        obesidade = random.choice(["Sim", "Não"])
        deficiencia = random.choice(["Sim", "Não"])
        dificuldadesVisuais = random.choice(["Sim", "Não"])
        dificuldadesAuditivas = random.choice(["Sim", "Não"])
        condicaoMedica = random.choice(["Sim", "Não"])  # Alterado para "Sim" ou "Não"
        
        cursor.execute('''INSERT INTO Cuidadores (
                            nome, idade, sexo, contato, endereco, mobilidade, obesidade, deficiencia, 
                            dificuldadesVisuais, dificuldadesAuditivas, condicaoMedica)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (nome, idade, sexo, contato, endereco, mobilidade, obesidade, deficiencia, 
                        dificuldadesVisuais, dificuldadesAuditivas, condicaoMedica))
    conn.commit()
    print(f"{n} cuidadores inseridos com sucesso.")

# Inserindo 10 cuidadores e 10 idosos com dados aleatórios
inserir_idosos_aleatorios(10)
inserir_cuidadores_aleatorios(10)

# Fechando a conexão com o banco de dados
conn.close()
