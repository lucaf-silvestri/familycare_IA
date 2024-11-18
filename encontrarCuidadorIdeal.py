import sqlite3
import pandas as pd
from sklearn.neighbors import NearestNeighbors


# Exemplo de como extrair dados de uma tabela e transformar em DataFrame
def carregar_dados():
    conn = sqlite3.connect('familycare.db')
    idosos_df = pd.read_sql_query("SELECT * FROM Idosos", conn)
    cuidadores_df = pd.read_sql_query("SELECT * FROM Cuidadores", conn)
    conn.close()
    return idosos_df, cuidadores_df


def recomendar_cuidador(idoso_dados, cuidadores_df):
    # Filtra os dados para apenas as colunas de interesse
    features = ["mobilidade", "obesidade", "deficiencia", "dificuldadesVisuais",
                "dificuldadesAuditivas", "condicaoMedica"]

    # Codificação das variáveis
    cuidadores_df_encoded = pd.get_dummies(cuidadores_df[features])
    idoso_encoded = pd.get_dummies(pd.DataFrame([idoso_dados], columns=features))

    # Ajustar dimensões, caso necessário
    cuidadores_df_encoded, idoso_encoded = cuidadores_df_encoded.align(idoso_encoded, fill_value=0, axis=1)

    # Treinar o modelo kNN
    knn = NearestNeighbors(n_neighbors=1)
    knn.fit(cuidadores_df_encoded)

    # Encontrar o cuidador mais próximo
    distancia, indice = knn.kneighbors(idoso_encoded)

    # Acessar o índice do cuidador recomendado
    indice_cuidador = indice[0][0]

    # Acessar o nome do cuidador recomendado diretamente usando o índice
    cuidador_recomendado = cuidadores_df.iloc[indice_cuidador]['nome']

    return cuidador_recomendado


def exibir_menu_de_idosos(idosos_df):
    # Exibir os idosos cadastrados e pedir ao usuário para escolher
    print("Escolha um dos idosos cadastrados:")
    for i, idoso in idosos_df.iterrows():
        print(f"{i + 1} - {idoso['nome']}")

    escolha = int(input("\nDigite o número do idoso para recomendar o cuidador: "))

    return idosos_df.iloc[escolha - 1]  # Retorna o idoso escolhido


def realizar_matching():
    idosos_df, cuidadores_df = carregar_dados()

    # Exibe o menu para o usuário escolher o idoso
    idoso_escolhido = exibir_menu_de_idosos(idosos_df)

    # Chama a função de recomendação de cuidador
    cuidador_recomendado = recomendar_cuidador(idoso_escolhido, cuidadores_df)

    print(f"\nCuidador recomendado para {idoso_escolhido['nome']}: {cuidador_recomendado}")


# Executando o matching
realizar_matching()