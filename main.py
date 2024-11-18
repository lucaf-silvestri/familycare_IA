from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import joblib
import json


# Carregar e treinar o modelo (caso necessário)
def train_model():
    data = pd.read_csv('feedbacks.csv')

    # Preparar dados
    X = data['feedback']
    y = data['classificacao']

    # Dividir os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Transformar texto em vetor
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Treinar modelo SVM
    model = SVC(kernel='linear')
    model.fit(X_train_vec, y_train)

    # Salvar modelo e vectorizer
    joblib.dump(model, 'data/modelo_svm.pkl')
    joblib.dump(vectorizer, 'data/vectorizer.pkl')

    print("Modelo treinado e salvo com sucesso.")


# Carregar o modelo treinado e o vectorizer
def load_model():
    model = joblib.load('modelo.pkl')
    return model


# Criar o app Flask
app = Flask(__name__)

# Carregar o modelo treinado e o vectorizer
model, vectorizer = load_model()

# Mapeamento de classificações
classificacao_mapping = {
    "Excelente": 4,
    "Bom": 3,
    "Mediano": 2,
    "Ruim": 1
}


@app.route('/classificar_feedback', methods=['POST'])
def classificar_feedback():
    data = request.get_json()

    if 'feedback' not in data or 'id_cuidador' not in data or 'id_avaliador' not in data:
        return jsonify({"error": "Dados incompletos"}), 400

    feedback = data['feedback']
    id_cuidador = data['id_cuidador']
    id_avaliador = data['id_avaliador']

    # Realizar a previsão
    classificacao = model.predict(vectorizer.transform([feedback]))[0]
    classificacao_numerica = classificacao_mapping[classificacao]

    # Aqui você pode adicionar a lógica para salvar a avaliação no banco de dados
    # atualizar_avaliacao_cuidador(id_cuidador, id_avaliador, classificacao_numerica)

    return jsonify({
        "classificacao": classificacao,
        "feedback": feedback,
        "id_avaliador": id_avaliador,
        "id_cuidador": id_cuidador
    })

if __name__ == "__main__":
    # Verifica se o modelo já existe, caso contrário, treina um novo modelo
    try:
        model = joblib.load('modelo_svm.pkl')
        print("Modelo carregado com sucesso.")
    except FileNotFoundError:
        print("Modelo não encontrado, treinando um novo modelo...")
        train_model()

    app.run(debug=True)
