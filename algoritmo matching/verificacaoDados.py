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
                print(f"ID: {idoso[0]}, Nome: {idoso[1]}, Idade: {idoso[2]}, Sexo: {idoso[3]}, Contato: {idoso[4]}, "
                      f"Endereço: {idoso[5]}, Mobilidade: {idoso[6]}, Obesidade: {idoso[7]}, Deficiência: {idoso[8]}, "
                      f"Dificuldades Visuais: {idoso[9]}, Dificuldades Auditivas: {idoso[10]}, Uso de Medicamentos: {idoso[11]}, "
                      f"Alimentação Assistida: {idoso[12]}, Higiene Assistida: {idoso[13]}, Alergias: {idoso[14]}, "
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
                print(f"ID: {cuidador[0]}, Nome: {cuidador[1]}, Idade: {cuidador[2]}, Sexo: {cuidador[3]}, "
                      f"Contato: {cuidador[4]}, Endereço: {cuidador[5]}, Mobilidade: {cuidador[6]}, "
                      f"Obesidade: {cuidador[7]}, Deficiência: {cuidador[8]}, Dificuldades Visuais: {cuidador[9]}, "
                      f"Dificuldades Auditivas: {cuidador[10]}, Condição Médica: {cuidador[11]}")
        else:
            print("Nenhum cuidador cadastrado encontrado.")

    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao acessar o banco de dados: {e}")

    # Fechando a conexão com o banco de dados
    conn.close()

    return cuidadores  # Retorna os dados dos cuidadores

def salvar_em_excel():
    # Buscar os dados
    idosos = buscar_idosos()
    cuidadores = buscar_cuidadores()

    # Criando dataframes a partir dos dados dos idosos e cuidadores
    colunas_idosos = ["ID", "Nome", "Idade", "Sexo", "Contato", "Endereço", "Mobilidade", "Obesidade", 
                      "Deficiência", "Dificuldades Visuais", "Dificuldades Auditivas", "Uso de Medicamentos", 
                      "Alimentação Assistida", "Higiene Assistida", "Alergias", "Condição Médica"]
    
    colunas_cuidadores = ["ID", "Nome", "Idade", "Sexo", "Contato", "Endereço", "Mobilidade", "Obesidade", 
                          "Deficiência", "Dificuldades Visuais", "Dificuldades Auditivas", "Condição Médica"]

    # Convertendo os dados para DataFrame
    df_idosos = pd.DataFrame(idosos, columns=colunas_idosos)
    df_cuidadores = pd.DataFrame(cuidadores, columns=colunas_cuidadores)

    # Salvando os dataframes como arquivos Excel
    with pd.ExcelWriter("dados_familycare.xlsx", engine='openpyxl') as writer:
        df_idosos.to_excel(writer, sheet_name='Idosos', index=False)
        df_cuidadores.to_excel(writer, sheet_name='Cuidadores', index=False)

    print("Planilhas Excel geradas com sucesso: 'dados_familycare.xlsx'.")

# Chamando a função para gerar as planilhas
salvar_em_excel()
