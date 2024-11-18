import sqlite3
from faker import Faker
import random

# Configurando Faker para gerar dados fictícios
fake = Faker("pt_BR")

# Conectando ao banco de dados
conn = sqlite3.connect('familycare.db')
cursor = conn.cursor()


def listar_cuidadores_por_avaliacao():
    conn = sqlite3.connect('familycare.db')
    cursor = conn.cursor()

    # Consulta que retorna todos os cuidadores ordenados pela média de suas avaliações (do melhor para o pior)
    cursor.execute('''SELECT C.id, C.nome, COUNT(A.id), AVG(A.classificacao) 
                      FROM Cuidadores C
                      LEFT JOIN Avaliacoes A ON C.id = A.id_cuidador
                      GROUP BY C.id
                      ORDER BY AVG(A.classificacao) DESC, COUNT(A.id) DESC''')

    cuidadores = cursor.fetchall()
    conn.close()

    return cuidadores


# Exemplo de uso:
cuidadores = listar_cuidadores_por_avaliacao()

# Exibindo os cuidadores do melhor para o pior
for cuidador in cuidadores:
    id_cuidador, nome, total_avaliacoes, media_classificacao = cuidador
    print(f"Cuidador: {nome} (ID: {id_cuidador})")
    print(f"Total de avaliações: {total_avaliacoes}")
    print(f"Média das classificações: {media_classificacao}\n")

# Criação das tabelas (Idosos, Cuidadores e Avaliacoes)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Idosos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
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
        email TEXT,
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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Avaliacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_idoso INTEGER,
        id_cuidador INTEGER,
        email_idoso TEXT,
        email_cuidador TEXT,
        classificacao INTEGER,
        feedback TEXT,
        FOREIGN KEY (id_idoso) REFERENCES Idosos(id),
        FOREIGN KEY (id_cuidador) REFERENCES Cuidadores(id),
        FOREIGN KEY (email_idoso) REFERENCES Idosos(email),
        FOREIGN KEY (email_cuidador) REFERENCES Cuidadores(email)
    )
''')


# Função para inserir idosos aleatórios
def inserir_idosos_aleatorios(n=10):
    for _ in range(n):
        nome = fake.name()
        email = fake.email()
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
        condicaoMedica = random.choice(["Sim", "Não"])

        cursor.execute('''INSERT INTO Idosos (
                            nome, email, idade, sexo, contato, endereco, mobilidade, obesidade, deficiencia,
                            dificuldadesVisuais, dificuldadesAuditivas, usoMedicamentos, alimentacaoAssistida, 
                            higieneAssistida, alergias, condicaoMedica)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (nome, email, idade, sexo, contato, endereco, mobilidade, obesidade, deficiencia,
                        dificuldadesVisuais, dificuldadesAuditivas, usoMedicamentos, alimentacaoAssistida,
                        higieneAssistida, alergias, condicaoMedica))
    conn.commit()


# Função para inserir cuidadores aleatórios
def inserir_cuidadores_aleatorios(n=10):
    for _ in range(n):
        nome = fake.name()
        email = fake.email()
        idade = random.randint(25, 60)
        sexo = random.choice(["Masculino", "Feminino"])
        contato = fake.phone_number()
        endereco = fake.address()
        mobilidade = random.choice(["Sim", "Não"])
        obesidade = random.choice(["Sim", "Não"])
        deficiencia = random.choice(["Sim", "Não"])
        dificuldadesVisuais = random.choice(["Sim", "Não"])
        dificuldadesAuditivas = random.choice(["Sim", "Não"])
        condicaoMedica = random.choice(["Sim", "Não"])

        cursor.execute('''INSERT INTO Cuidadores (
                            nome, email, idade, sexo, contato, endereco, mobilidade, obesidade, deficiencia, 
                            dificuldadesVisuais, dificuldadesAuditivas, condicaoMedica)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (nome, email, idade, sexo, contato, endereco, mobilidade, obesidade, deficiencia,
                        dificuldadesVisuais, dificuldadesAuditivas, condicaoMedica))
    conn.commit()


# Inserindo 10 cuidadores e 10 idosos com dados aleatórios
inserir_idosos_aleatorios(11)
inserir_cuidadores_aleatorios(11)

# Fechando a conexão com o banco de dados
conn.close()
