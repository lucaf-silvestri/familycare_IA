import sqlite3
import pandas as pd

def buscar_idosos():
    # Conectando ao banco de dados
    conn = sqlite3.connect('familycare.db')
    cursor = conn.cursor()

    # Executando a consulta para selecionar todos os idosos (todos os campos)
    try:
        cursor.execute("SELECT * FROM Idosos")  # Usando o nome correto da tabela 'Idosos'
        idosos = cursor.fetchall()

        if idosos:
            print("Idosos cadastrados:")
            for idoso in idosos:
                # Imprimindo todos os campos dos idosos
                print(f"ID: {idoso[0]}, Nome: {idoso[1]}, Email:{idoso[2]}, Idade: {idoso[3]}, Sexo: {idoso[4]}, Contato: {idoso[5]}, "
                      f"Endereço: {idoso[6]}, Mobilidade: {idoso[7]}, Obesidade: {idoso[8]}, Deficiência: {idoso[9]}, "
                      f"Dificuldades Visuais: {idoso[10]}, Dificuldades Auditivas: {idoso[11]}, Uso de Medicamentos: {idoso[12]}, "
                      f"Alimentação Assistida: {idoso[13]}, Higiene Assistida: {idoso[14]}, Alergias: {idoso[15]}, "
                      f"Condição Médica: {idoso[15]}")
        else:
            print("Nenhum idoso cadastrado encontrado.")

    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao acessar o banco de dados: {e}")

    # Fechando a conexão com o banco de dados
    conn.close()

    return idosos  # Retorna os dados dos idosos

def buscar_cuidadores():
    # Conectando ao banco de dados
    conn = sqlite3.connect('familycare.db')
    cursor = conn.cursor()

    # Executando a consulta para selecionar todos os cuidadores (todos os campos)
    try:
        cursor.execute("SELECT * FROM Cuidadores")  # Usando o nome correto da tabela 'Cuidadores'
        cuidadores = cursor.fetchall()

        if cuidadores:
            print("Cuidadores cadastrados:")
            for cuidador in cuidadores:
                # Imprimindo todos os campos dos cuidadores
                print(f"ID: {cuidador[0]}, Nome: {cuidador[1]}, Email:{cuidador[2]}, Idade: {cuidador[3]}, Sexo: {cuidador[4]}, "
                      f"Contato: {cuidador[5]}, Endereço: {cuidador[6]}, Mobilidade: {cuidador[7]}, "
                      f"Obesidade: {cuidador[8]}, Deficiência: {cuidador[9]}, Dificuldades Visuais: {cuidador[10]}, "
                      f"Dificuldades Auditivas: {cuidador[11]}, Condição Médica: {cuidador[12]}")
        else:
            print("Nenhum cuidador cadastrado encontrado.")

    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao acessar o banco de dados: {e}")

    # Fechando a conexão com o banco de dados
    conn.close()

    return cuidadores  # Retorna os dados dos cuidadores

def buscar_avaliacoes():
    # Conectando ao banco de dados
    conn = sqlite3.connect('familycare.db')
    cursor = conn.cursor()

    # Executando a consulta para selecionar todas as avaliações
    try:
        cursor.execute("SELECT * FROM Avaliacoes")  # Usando o nome correto da tabela 'Avaliacoes'
        avaliacoes = cursor.fetchall()

        if avaliacoes:
            print("Avaliações registradas:")
            for avaliacao in avaliacoes:
                # Imprimindo todos os campos das avaliações
                print(f"ID: {avaliacao[0]}, ID Idoso: {avaliacao[1]}, ID Cuidador: {avaliacao[2]}, Email Idoso: {avaliacao[3]}, "
                      f"Email Cuidador: {avaliacao[4]}, Classificação: {avaliacao[5]}, Feedback: {avaliacao[6]}")
        else:
            print("Nenhuma avaliação registrada encontrada.")

    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao acessar o banco de dados: {e}")

    # Fechando a conexão com o banco de dados
    conn.close()

    return avaliacoes  # Retorna as avaliações

def salvar_em_excel():
    # Buscar os dados
    idosos = buscar_idosos()
    cuidadores = buscar_cuidadores()
    avaliacoes = buscar_avaliacoes()

    # Criando dataframes a partir dos dados dos idosos e cuidadores
    colunas_idosos = ["ID", "Nome", "Email", "Idade", "Sexo", "Contato", "Endereço", "Mobilidade", "Obesidade",
                      "Deficiência", "Dificuldades Visuais", "Dificuldades Auditivas", "Uso de Medicamentos", 
                      "Alimentação Assistida", "Higiene Assistida", "Alergias", "Condição Médica", "Senha"]
    
    colunas_cuidadores = ["ID", "Nome", "Email", "Idade", "Sexo", "Contato", "Endereço", "Mobilidade", "Obesidade",
                          "Deficiência", "Dificuldades Visuais", "Dificuldades Auditivas", "Condição Médica", "Senha"]

    colunas_avaliacoes = ["ID", "ID Idoso", "ID Cuidador", "Email Idoso", "Email Cuidador", "Classificação", "Feedback"]


    # Convertendo os dados para DataFrame
    df_idosos = pd.DataFrame(idosos, columns=colunas_idosos)
    df_cuidadores = pd.DataFrame(cuidadores, columns=colunas_cuidadores)
    df_avaliacoes = pd.DataFrame(avaliacoes, columns=colunas_avaliacoes)


    # Salvando os dataframes como arquivos Excel
    with pd.ExcelWriter("dados_familycare.xlsx", engine='openpyxl') as writer:
        df_idosos.to_excel(writer, sheet_name='Idosos', index=False)
        df_cuidadores.to_excel(writer, sheet_name='Cuidadores', index=False)
        df_avaliacoes.to_excel(writer, sheet_name='Avaliações', index=False)

    print("Planilhas Excel geradas com sucesso: 'dados_familycare.xlsx'.")

# Chamando a função para gerar as planilhas
salvar_em_excel()
