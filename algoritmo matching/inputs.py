# Programa permite que o usuário cadastre idosos e cuidadores 

import sqlite3
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Conexão com o banco de dados SQLite
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
conn.commit()

def coletar_dados_idoso():
    print("\nCadastro do idoso no aplicativo FamilyCare.")

    nomeIdoso = input("\nNome completo do idoso: ")
    idadeIdoso = input("Idade: ")
    sexoIdoso = input("Sexo (M/F): ")
    sexoValido = False

    while not sexoValido:
        if sexoIdoso.lower() == "m":
            sexoIdoso = "Masculino"
            sexoValido = True
        elif sexoIdoso.lower() == "f":
            sexoIdoso = "Feminino"
            sexoValido = True
        else:
            sexoIdoso = input("Adicione um sexo válido (M/F): ")

    contatoIdoso = input("Telefone de contato: ")
    enderecoIdoso = input("Endereço: ")

    print("\nInformações sobre dificuldades e cuidados")
    
    def validar_resposta(pergunta):
        resposta = input(pergunta).strip().lower()
        return "Sim" if resposta == "s" else "Não"

    mobilidadeIdoso = validar_resposta("O idoso precisa de ajuda para andar? (S/N): ")
    obesidadeIdoso = validar_resposta("O idoso é obeso? (S/N): ")
    deficienciaIdoso = validar_resposta("O idoso possui alguma deficiência física? (S/N): ")
    dificuldadesVisuaisIdoso = validar_resposta("O idoso possui dificuldades visuais? (S/N): ")
    dificuldadesAuditivasIdoso = validar_resposta("O idoso possui dificuldades auditivas? (S/N): ")
    usoMedicamentosIdoso = validar_resposta("O idoso faz uso de medicamentos diários? (S/N): ")
    alimentacaoAssistidaIdoso = validar_resposta("O idoso precisa de ajuda para se alimentar? (S/N): ")
    higieneAssistidaIdoso = validar_resposta("O idoso precisa de ajuda para higiene pessoal? (S/N): ")
    possuiAlergiasIdoso = validar_resposta("O idoso possui alergias? (S/N): ")
    condicaoMedicaIdoso = validar_resposta("O idoso possui alguma condição médica grave? (S/N): ")

    # Resumo das informações coletadas
    print("\nResumo das Informações do Idoso")
    print(f"Nome: {nomeIdoso}")
    print(f"Idade: {idadeIdoso}")
    print(f"Sexo: {sexoIdoso}")
    print(f"Telefone de contato: {contatoIdoso}")
    print(f"Endereço: {enderecoIdoso}")
    print(f"Ajuda para andar: {mobilidadeIdoso}")
    print(f"Obesidade: {obesidadeIdoso}")
    print(f"Deficiência física: {deficienciaIdoso}")
    print(f"Dificuldades visuais: {dificuldadesVisuaisIdoso}")
    print(f"Dificuldades auditivas: {dificuldadesAuditivasIdoso}")
    print(f"Uso de medicamentos: {usoMedicamentosIdoso}")
    print(f"Ajuda para se alimentar: {alimentacaoAssistidaIdoso}")
    print(f"Ajuda para higiene pessoal: {higieneAssistidaIdoso}")
    print(f"Alergias: {possuiAlergiasIdoso}")
    print(f"Condição médica grave: {condicaoMedicaIdoso}")

    dadosIdoso = {
        "nomeIdoso": nomeIdoso,
        "idadeIdoso": idadeIdoso,
        "sexoIdoso": sexoIdoso,
        "contatoIdoso": contatoIdoso,
        "enderecoIdoso": enderecoIdoso,
        "mobilidadeIdoso": mobilidadeIdoso,
        "obesidadeIdoso": obesidadeIdoso,
        "deficienciaIdoso": deficienciaIdoso,
        "dificuldadesVisuaisIdoso": dificuldadesVisuaisIdoso,
        "dificuldadesAuditivasIdoso": dificuldadesAuditivasIdoso,
        "usoMedicamentosIdoso": usoMedicamentosIdoso,
        "alimentacaoAssistidaIdoso": alimentacaoAssistidaIdoso,
        "higieneAssistidaIdoso": higieneAssistidaIdoso,
        "possuiAlergiasIdoso": possuiAlergiasIdoso,
        "condicaoMedicaIdoso": condicaoMedicaIdoso
    }

    print("\nInformações coletadas com sucesso!")
    return dadosIdoso

def coletar_dados_cuidador():
    print("\nCadastro do cuidador no aplicativo FamilyCare.")

    nomeCuidador = input("\nNome completo do cuidador: ")
    idadeCuidador = input("Idade: ")
    sexoCuidador = input("Sexo (M/F): ")
    sexoValido = False

    while not sexoValido:
        if sexoCuidador.lower() == "m":
            sexoCuidador = "Masculino"
            sexoValido = True
        elif sexoCuidador.lower() == "f":
            sexoCuidador = "Feminino"
            sexoValido = True
        else:
            sexoCuidador = input("Adicione um sexo válido (M/F): ")

    contatoCuidador = input("Telefone de contato: ")
    enderecoCuidador = input("Endereço: ")

    print("\nInformações sobre habilidades e capacidades")
    mobilidadeCuidador = "Sim" if input("O cuidador tem capacidade de carregar o idoso, se necessário? (S/N): ").upper() == "S" else "Não"
    obesidadeCuidador = "Sim" if input("O cuidador tem capacidade de trabalhar com idosos com obesidade? (S/N): ").upper() == "S" else "Não"
    deficienciaCuidador = "Sim" if input("O cuidador tem capacidade de trabalhar com idosos deficientes? (S/N): ").upper() == "S" else "Não"
    
    dificuldadesVisuaisCuidador = "Sim" if input("O cuidador tem capacidade de trabalhar com idosos com dificuldades visuais? (S/N): ").upper() == "S" else "Não"
    dificuldadesAuditivasCuidador = "Sim" if input("O cuidador tem capacidade de trabalhar com idosos com dificuldades auditivas? (S/N): ").upper() == "S" else "Não"
    condicaoMedicaCuidador = "Sim" if input("O cuidador tem capacidade de trabalhar com idosos com condições médicas graves? (S/N): ").upper() == "S" else "Não"

    # Resumo das informações coletadas
    print("\nResumo das Informações do Cuidador")
    print(f"Nome: {nomeCuidador}")
    print(f"Idade: {idadeCuidador}")
    print(f"Sexo: {sexoCuidador}")
    print(f"Telefone de contato: {contatoCuidador}")
    print(f"Endereço: {enderecoCuidador}")
    print(f"Capaz de auxiliar o idoso a andar: {mobilidadeCuidador}")
    print(f"Capaz de lidar com idosos com obesidade: {obesidadeCuidador}")
    print(f"Capaz de lidar com idosos com deficiência física: {deficienciaCuidador}")
    print(f"Capaz de lidar com idosos com dificuldades visuais: {dificuldadesVisuaisCuidador}")
    print(f"Capaz de lidar com idosos com dificuldades auditivas: {dificuldadesAuditivasCuidador}")
    print(f"Capaz de lidar com idosos com condição médica grave: {condicaoMedicaCuidador}")

    dadosCuidador = {
        "nomeCuidador": nomeCuidador,
        "idadeCuidador": idadeCuidador,
        "sexoCuidador": sexoCuidador,
        "contatoCuidador": contatoCuidador,
        "enderecoCuidador": enderecoCuidador,
        "mobilidadeCuidador": mobilidadeCuidador,
        "obesidadeCuidador": obesidadeCuidador,
        "deficienciaCuidador": deficienciaCuidador,
        "dificuldadesVisuaisCuidador": dificuldadesVisuaisCuidador,
        "dificuldadesAuditivasCuidador": dificuldadesAuditivasCuidador,
        "condicaoMedicaCuidador": condicaoMedicaCuidador
    }

    print("\nInformações coletadas com sucesso!")
    return dadosCuidador

def salvar_dados_idoso(dadosIdoso):
    conn = sqlite3.connect('familycare.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Idosos (nome, idade, sexo, contato, endereco, mobilidade, obesidade, deficiencia,
                            dificuldadesVisuais, dificuldadesAuditivas, usoMedicamentos, alimentacaoAssistida,
                            higieneAssistida, alergias, condicaoMedica)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (dadosIdoso["nomeIdoso"], dadosIdoso["idadeIdoso"], dadosIdoso["sexoIdoso"], dadosIdoso["contatoIdoso"],
          dadosIdoso["enderecoIdoso"], dadosIdoso["mobilidadeIdoso"], dadosIdoso["obesidadeIdoso"], dadosIdoso["deficienciaIdoso"],
          dadosIdoso["dificuldadesVisuaisIdoso"], dadosIdoso["dificuldadesAuditivasIdoso"], dadosIdoso["usoMedicamentosIdoso"],
          dadosIdoso["alimentacaoAssistidaIdoso"], dadosIdoso["higieneAssistidaIdoso"], dadosIdoso["possuiAlergiasIdoso"],
          dadosIdoso["condicaoMedicaIdoso"]))
    conn.commit()
    conn.close()
    print("Dados do idoso salvos com sucesso!")

def salvar_dados_cuidador(dadosCuidador):
    conn = sqlite3.connect('familycare.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Cuidadores (nome, idade, sexo, contato, endereco, mobilidade, obesidade, deficiencia,
                                dificuldadesVisuais, dificuldadesAuditivas, condicaoMedica)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (dadosCuidador["nomeCuidador"], dadosCuidador["idadeCuidador"], dadosCuidador["sexoCuidador"], dadosCuidador["contatoCuidador"],
          dadosCuidador["enderecoCuidador"], dadosCuidador["mobilidadeCuidador"], dadosCuidador["obesidadeCuidador"], dadosCuidador["deficienciaCuidador"],
          dadosCuidador["dificuldadesVisuaisCuidador"], dadosCuidador["dificuldadesAuditivasCuidador"], dadosCuidador["condicaoMedicaCuidador"]))
    conn.commit()
    conn.close()
    print("Dados do cuidador salvos com sucesso!")

repetirMenu = True

while repetirMenu == True:
    escolha = int(input("\nEscolha o tipo de usuário que deseja cadastrar: \n1 - Idoso\n2 - Cuidador\n3 - Sair\n"))
    
    if escolha == 1:
        dadosIdoso = coletar_dados_idoso()
        salvar_dados_idoso(dadosIdoso)
    elif escolha == 2:
        dadosCuidador = coletar_dados_cuidador()
        salvar_dados_cuidador(dadosCuidador)
    elif escolha == 3:
        repetirMenu = False
    else:
        print("Você não escolheu uma opção válida.\n")