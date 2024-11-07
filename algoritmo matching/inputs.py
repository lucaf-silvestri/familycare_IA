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
    mobilidadeIdoso = input("O idoso precisa de ajuda para andar? (S/N): ")
    obesidadeIdoso = input("O idoso é obeso? (S/N): ")
    deficienciaIdoso = input("O idoso possui alguma deficiência física? (S/N): ")

    dificuldadesVisuaisIdoso = input("O idoso possui dificuldades visuais? (S/N): ")
    dificuldadesAuditivasIdoso = input("O idoso possui dificuldades auditivas? (S/N): ")
    usoMedicamentosIdoso = input("O idoso faz uso de medicamentos diários? (S/N): ")

    alimentacaoAssistidaIdoso = input("O idoso precisa de ajuda para se alimentar? (S/N): ")
    higieneAssistidaIdoso = input("O idoso precisa de ajuda para higiene pessoal? (S/N): ")
    possuiAlergiasIdoso = input("O idoso possui alergias? (S/N): ")

    condicaoMedicaIdoso = input("O idoso possui alguma condição médica grave? (S/N): ")

    # Resumo das informações coletadas
    print("\nResumo das Informações do Idoso")
    print(f"Nome: {nomeIdoso}")
    print(f"Idade: {idadeIdoso}")
    print(f"Sexo: {sexoIdoso}")
    print(f"Telefone de contato: {contatoIdoso}")
    print(f"Endereço: {enderecoIdoso}")
    print(f"Ajuda para andar: {'Sim' if mobilidadeIdoso.upper() == 'S' else 'Não'}")
    print(f"Obesidade: {'Sim' if obesidadeIdoso.upper() == 'S' else 'Não'}")
    print(f"Deficiência física: {'Sim' if deficienciaIdoso.upper() == 'S' else 'Não'}")
    print(f"Dificuldades visuais: {'Sim' if dificuldadesVisuaisIdoso.upper() == 'S' else 'Não'}")
    print(f"Dificuldades auditivas: {'Sim' if dificuldadesAuditivasIdoso.upper() == 'S' else 'Não'}")
    print(f"Uso de medicamentos: {'Sim' if usoMedicamentosIdoso.upper() == 'S' else 'Não'}")
    print(f"Ajuda para se alimentar: {'Sim' if alimentacaoAssistidaIdoso.upper() == 'S' else 'Não'}")
    print(f"Ajuda para higiene pessoal: {'Sim' if higieneAssistidaIdoso.upper() == 'S' else 'Não'}")
    print(f"Alergias: {'Sim' if possuiAlergiasIdoso.upper() == 'S' else 'Não'}")
    print(f"Condição médica grave: {'Sim' if condicaoMedicaIdoso.upper() == 'S' else 'Não'}")

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

    while sexoValido == False:
        if sexoCuidador == "m" or sexoCuidador =="M":
            sexoCuidador = "Masculino"
            sexoValido = True
        elif sexoCuidador == "f" or sexoCuidador =="F":
            sexoCuidador = "Feminino"
            sexoValido = True
        else:
            sexoCuidador = input("Adicione um sexo válido (M/F):")

    contatoCuidador = input("Telefone de contato: ")
    enderecoCuidador = input("Endereço: ")

    print("\nInformações sobre habilidades e capacidades")
    mobilidadeCuidador = input("O cuidador tem capacidade de carregar o idoso, se necessário? (S/N): ")
    obesidadeCuidador = input("O cuidador tem capacidade de trabalhar com idosos com obesidade? (S/N): ")
    deficienciaCuidador = input("O cuidador tem capacidade de trabalhar com idosos deficientes? (S/N): ")

    dificuldadesVisuaisCuidador = input("O cuidador tem capacidade de trabalhar com idosos com dificuldades visuais? (S/N): ")
    dificuldadesAuditivasCuidador = input("O cuidador tem capacidade de trabalhar com idosos com dificuldades auditivas? (S/N): ")

    condicaoMedicaCuidador = input("O cuidador tem capacidade de trabalhar com idosos com condições médicas graves? (S/N): ")

    # Resumo das informações coletadas
    print("\nResumo das Informações do Cuidador")
    print(f"Nome: {nomeCuidador}")
    print(f"Idade: {idadeCuidador}")
    print(f"Sexo: {sexoCuidador}")
    print(f"Telefone de contato: {contatoCuidador}")
    print(f"Endereço: {enderecoCuidador}")
    print(f"Capaz de auxiliar o idoso a andar: {'Sim' if mobilidadeCuidador.upper() == 'S' else 'Não'}")
    print(f"Capaz de lidar com idosos com obesidade: {'Sim' if obesidadeCuidador.upper() == 'S' else 'Não'}")
    print(f"Capaz de lidar com idosos com deficiência física: {'Sim' if deficienciaCuidador.upper() == 'S' else 'Não'}")
    print(f"Capaz de lidar com idosos com dificuldades visuais: {'Sim' if dificuldadesVisuaisCuidador.upper() == 'S' else 'Não'}")
    print(f"Capaz de lidar com idosos com dificuldades auditivas: {'Sim' if dificuldadesAuditivasCuidador.upper() == 'S' else 'Não'}")
    print(f"Capaz de lidar com idosos com condição médica grave: {'Sim' if condicaoMedicaCuidador.upper() == 'S' else 'Não'}")
    
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