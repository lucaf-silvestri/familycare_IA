import sqlite3
import joblib
import json
from flask import Flask, request, jsonify
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

feedbacks_excelente = [
    # Excelente (100 exemplos)
    "Excelente trabalho, muito bom", "Atendimento perfeito", "Muito satisfeito, ótimo serviço",
    "Fiquei muito feliz com o resultado", "Excelente experiência", "Muito bom, gostei muito",
    "Maravilhoso, super recomendo", "Fantástico, superou as expectativas", "Impecável, perfeito",
    "Adorei, tudo perfeito", "Excelente, continue assim", "Muito bom, não tenho palavras",
    "Perfeito, foi ótimo", "Excelente cuidado, adorei", "Ótimo serviço", "Muito bom, sem reclamações",
    "Melhor experiência que já tive", "Amei, muito bom", "Excelente atendimento, super recomendo",
    "Perfeito, tudo ótimo", "Simplesmente excelente", "Excelente, faria de novo", "Tudo muito bem feito",
    "Muito bom, vou indicar para os amigos", "Excelente, voltarei com certeza", "Maravilhoso, adorei",
    "Muito bom, adorei o atendimento", "Excelente, mais que satisfatório", "Ótimo, estou satisfeito",
    "Impecável, muito bom", "Perfeito, amei", "Excelente cuidado, muito bem feito", "Fiquei impressionado, excelente",
    "A experiência foi excelente", "Adorei, foi maravilhoso", "Muito bom, ótimo cuidado", "Atendimento excelente",
    "Muito bom, gostei muito", "Excelente, recomendo sem dúvida", "Tudo perfeito", "Simplesmente ótimo",
    "Foi maravilhoso, recomendo", "Excelente, realmente bom", "Perfeito, estou muito satisfeito",
    "Excelente atendimento, sem palavras", "Ótimo, recomendo a todos", "Muito bom, sou grato",
    "Perfeito, nunca tive um atendimento tão bom", "Excelente, não tem como melhorar", "Fiquei muito satisfeito",
    "Ótimo, atendeu todas as minhas expectativas", "Excelente, tudo maravilhoso", "Muito bom, bem feito",
    "Adorei, maravilhoso", "Foi perfeito", "Excelente, gostei muito", "Atendimento excelente, tudo ótimo",
    "A experiência foi ótima, superou minhas expectativas", "Muito bom, recomendo com certeza",
    "Excelente, melhor do que imaginava", "Muito bom, adorei tudo", "Maravilhoso, 100%", "Ótimo serviço, tudo perfeito",
    "Excelente trabalho, agradeço muito", "Super recomendo, excelente", "Muito bom, ótimo atendimento",
    "Excelente, gostei de tudo", "Tudo excelente, gostei demais", "Maravilhoso, sem defeitos",
    "Excelente, atendimento top", "Tudo ótimo, super recomendo", "Excelente, melhor do que imaginava",
    "Excelente, sem palavras", "Muito bom, perfeito", "Excelente, vou voltar sempre", "Ótimo atendimento",
    "Muito bom, muito satisfeito", "Excelente, serviço 100%", "Atendimento incrível, tudo maravilhoso",
    "Muito bom, recomendo", "Excelente, muito bem feito", "Perfeito, maravilhoso", "Excelente atendimento, gostei muito",
    "Ótimo, estou super satisfeito", "Muito bom, nada a reclamar", "Excelente, foi tudo perfeito",
    "Super recomendo, excelente", "Muito bom, adorei", "Excelente, top de linha", "Atendimento perfeito",
    "Tudo ótimo, muito bom", "Excelente, recomendo demais", "Perfeito, excelente experiência",
    "Excelente, atendimento impecável", "Muito bom, adorei muito", "Ótimo, sem palavras",
    "Excelente, muito satisfeito", "Perfeito, sem defeitos", "Amei, muito bom", "Excelente experiência",
    "Ótimo, recomendo bastante", "Excelente, melhor impossível", "Perfeito, tudo maravilhoso",
    "Excelente, superou as expectativas", "Atendimento top, excelente", "Muito bom, sem falhas",
    "Excelente, estive muito bem atendido", "Ótimo, maravilhoso", "Excelente, vou voltar sempre",
    "Excelente, um ótimo atendimento", "Super recomendo, excelente", "Muito bom, estou satisfeito",
    "Ótimo, muito bem feito", "Excelente, tudo ótimo", "Perfeito, melhor do que eu imaginava",
    "Muito bom, ótimo", "Excelente, sem dúvida", "Atendimento maravilhoso, tudo muito bom",
    "Muito bom, gostei muito", "Excelente, estou super satisfeito", "Muito bom, tudo excelente",
    "Excelente, recomendo com certeza"
]

labels_excellent = ["Excelente"] * len(feedbacks_excelente)

feedbacks_bom = [
    "Bom trabalho, mas pode melhorar", "Gostei, porém há alguns pontos a melhorar", "Bom serviço, mas precisa de ajustes",
    "Atendimento bom, mas não perfeito", "Serviço bom, mas com alguns detalhes", "Bom, mas poderia ser melhor",
    "Bom, mas com pequenas falhas", "Bom atendimento, mas poderia ser mais rápido", "Satisfeito com o serviço",
    "Bom, mas tem espaço para melhoria", "Atendimento bom, poderia ser mais personalizado", "Bom, gostei, mas não foi perfeito",
    "Bom, gostei do atendimento", "Bom serviço, mas não impecável", "Bom, mas houve demora", "Atendimento bom",
    "Gostei do serviço, mas pode melhorar", "Bom, nada a reclamar, mas também nada extraordinário", "Bom serviço",
    "Bom atendimento, não há muito a reclamar", "O serviço foi bom, mas sem grandes surpresas", "Bom, mas não é excelente",
    "Bom, mas alguns aspectos não foram tão bons", "Serviço bom, mas há necessidade de aprimoramento",
    "Gostei, mas não foi tudo perfeito", "Bom, mas seria bom se fosse mais rápido", "Bom, mas tem espaço para melhorar",
    "Bom, gostei do atendimento", "Atendimento bom, mas não é algo que me surpreendeu", "Bom, sem maiores problemas",
    "Serviço bom, mas não está no nível dos melhores", "Bom, gostei do resultado final", "Atendimento bom, mas com falhas",
    "Bom, mas esperava mais", "O atendimento foi bom", "Bom serviço, mas pode ser mais eficiente",
    "Gostei, mas foi algo normal", "Serviço bom, poderia ser mais rápido", "Bom, atendeu minhas expectativas",
    "Gostei do trabalho, mas há detalhes para melhorar", "Bom, com alguns pontos a serem trabalhados", "Bom, sem grandes problemas",
    "Atendimento bom, mas sem emoção", "Bom, mas poderia ser melhor", "Serviço bom, nada de extraordinário",
    "Bom, mas com algumas falhas", "Bom, mas o atendimento demorou um pouco", "Serviço bom, mas não incrível",
    "Gostei, mas o serviço não foi o melhor", "Bom, mas nada excepcional", "O atendimento foi bom, mas poderia ser mais rápido",
    "Bom, sem muitas surpresas", "Atendimento bom, sem reclamações", "Bom serviço, mas precisa melhorar",
    "Bom, gostei, mas não superou minhas expectativas", "Bom, mas poderia ser mais eficaz",
    "Bom atendimento, mas o serviço deixou a desejar", "Gostei do atendimento, mas o serviço não foi perfeito",
    "Bom, mas a experiência poderia ter sido melhor", "Serviço bom, mas o tempo de espera foi longo",
    "Bom, mas não foi algo memorável", "Gostei, mas não me impressionou", "Bom, poderia ser mais rápido",
    "Bom, gostei, mas não foi nada de incrível", "Serviço bom, mas a experiência foi regular",
    "Bom, mas o serviço foi um pouco demorado", "Bom, nada de excepcional", "Gostei, mas não foi a melhor experiência",
    "Bom, mas com algumas falhas", "Atendimento bom, mas não foi perfeito", "Bom, poderia ter sido melhor",
    "Gostei, mas poderia ser mais eficiente", "Bom, mas algumas áreas precisam de ajustes", "Atendimento bom, mas sem detalhes",
    "Bom, mas não superou o esperado", "Bom, gostei, mas não é a melhor experiência",
    "Serviço bom, mas poderia ser mais preciso", "Bom, mas deixou a desejar em alguns pontos", "Bom, gostei, mas não é incrível",
    "Atendimento bom, mas não surpreendeu", "Bom, gostei, mas poderia ser melhor", "Serviço bom", "Atendimento bom",
    "Bom serviço, mas ainda tem falhas", "Bom, mas não foi a experiência dos sonhos", "Gostei, mas não foi excepcional",
    "Serviço bom, mas faltou algo", "Bom, sem grandes expectativas", "Gostei, mas não foi o melhor serviço",
    "Bom, não há muito o que reclamar", "Serviço bom, mas não foi excepcional", "Bom, mas o atendimento poderia ser melhor",
    "Gostei, mas poderia ser mais rápido", "Bom, sem grandes surpresas", "Serviço bom, mas pode melhorar",
    "Bom, mas o atendimento foi um pouco frio", "Gostei, mas não foi algo impressionante", "Bom atendimento",
    "Serviço bom, mas não tem um toque especial", "Bom serviço", "Gostei do atendimento", "Serviço bom, mas sem grandes surpresas",
    "Gostei do trabalho, mas não foi excepcional", "Bom, sem muito a reclamar", "Serviço bom, mas ainda há pontos a melhorar",
    "Gostei do atendimento", "Bom, mas faltou algo", "Bom, sem surpresas", "Atendimento bom", "Bom serviço"
]

labels_bom = ["Bom"] * len(feedbacks_bom)

feedbacks_medio = [
    "O serviço foi regular, nada de mais", "Atendimento razoável, poderia ser melhor",
    "Não foi bom nem ruim, apenas ok", "O trabalho foi aceitável, mas não ótimo",
    "O serviço foi mediano, sem muitos elogios", "Atendimento bom, mas poderia ser mais atento",
    "Satisfeito, mas sem grandes expectativas", "O trabalho foi suficiente, nada fora do comum",
    "O serviço foi mediano, não tenho reclamações, mas também não foi ótimo", "Serviço mediano, pode melhorar",
    "Gostei, mas não foi excepcional", "Foi um atendimento razoável", "Não foi o melhor, mas também não foi ruim",
    "O serviço foi bom, mas não se destacou", "O atendimento foi bom, mas um pouco lento",
    "O trabalho foi bom, mas com algumas falhas", "Atendimento razoável, poderia ser mais ágil",
    "Foi um trabalho sem grandes surpresas", "O atendimento foi bom, mas poderia ser mais personalizado",
    "Foi uma experiência ok, sem grandes expectativas", "O serviço foi aceitável, mas não encantou",
    "Mediano, nada a reclamar, mas também nada de incrível", "Serviço mediano, poderia ser melhor",
    "Atendimento ok, mas nada impressionante", "Foi bom, mas sem nada de extraordinário",
    "Gostei, mas ficou a desejar em alguns pontos", "Não foi ruim, mas também não foi excelente",
    "O atendimento foi bom, mas não surpreendeu", "O serviço foi apenas suficiente",
    "Atendimento razoável, poderia ser mais rápido", "Serviço ok, mas não foi o melhor",
    "O trabalho foi bom, mas poderia ter sido melhor", "O serviço foi simples, mas eficaz",
    "Foi uma experiência neutra, nada muito bom nem ruim", "Gostei, mas não foi excelente",
    "Foi bom, mas com alguns pontos negativos", "O trabalho foi razoável, mas não foi perfeito",
    "O atendimento foi bom, mas faltou algo", "O serviço foi bom, mas a experiência poderia ser melhor",
    "Foi um bom atendimento, mas não foi excepcional", "Serviço razoável, poderia ser mais ágil",
    "Atendimento bom, mas não foi o melhor", "O serviço foi ok, nada fora do comum",
    "O trabalho foi bom, mas não foi incrível", "Atendimento mediano, sem falhas",
    "O serviço foi bom, mas poderia ter sido mais rápido", "Foi uma experiência ok, mas com falhas",
    "Gostei do serviço, mas poderia ser melhor", "O atendimento foi bom, mas faltou mais atenção",
    "O trabalho foi ok, mas não foi memorável", "Gostei, mas o serviço ficou a desejar em alguns pontos",
    "O serviço foi satisfatório, mas não encantou", "O atendimento foi bom, mas poderia ser mais eficiente",
    "O trabalho foi bom, mas não tem um toque especial", "Serviço ok, mas falta brilho",
    "Foi uma boa experiência, mas não maravilhosa", "Atendimento bom, mas sem grandes expectativas",
    "O serviço foi razoável, poderia ser mais rápido", "Foi bom, mas faltou mais atenção aos detalhes",
    "O trabalho foi mediano, poderia ser mais eficiente", "Foi ok, sem grandes reclamações",
    "O serviço foi simples, mas eficaz", "Atendimento bom, mas sem muito entusiasmo",
    "Gostei, mas o serviço poderia ser mais dedicado", "Foi bom, mas ficou a desejar em alguns aspectos",
    "O trabalho foi bom, mas a experiência poderia ser melhor", "Foi uma experiência mediana, sem surpresas",
    "O serviço foi bom, mas poderia ser mais eficiente", "O atendimento foi razoável, mas não se destacou",
    "Serviço bom, mas não foi uma experiência excelente", "Gostei do serviço, mas poderia ser mais rápido",
    "O atendimento foi ok, mas não foi excepcional", "O serviço foi bom, mas faltou um toque pessoal",
    "O trabalho foi bom, mas poderia ser mais detalhado", "Gostei, mas a experiência não foi tão boa",
    "O atendimento foi bom, mas sem muita emoção", "O serviço foi razoável, sem grandes falhas",
    "Atendimento ok, mas não se destacou", "Gostei do serviço, mas não me impressionou",
    "O trabalho foi bom, mas poderia ser mais rápido", "O serviço foi mediano, não tenho grandes elogios",
    "Foi ok, mas a experiência foi um pouco fria", "O atendimento foi bom, mas poderia ter sido mais eficaz",
    "Serviço bom, mas faltou algo a mais", "Gostei, mas faltou um toque especial", "O trabalho foi bom, mas não excelente"
]
labels_medio = ["Médio"] * len(feedbacks_medio)

feedbacks_ruim = [
    "O atendimento foi ruim, fiquei insatisfeito", "Serviço ruim, não recomendo",
    "A experiência foi decepcionante, não gostei", "O trabalho foi abaixo das expectativas",
    "Foi ruim, não valeu a pena", "Não gostei, não foi bom", "Serviço ruim, me decepcionou",
    "O atendimento foi demorado e insatisfatório", "Fiquei desapontado com o serviço",
    "Não gostei, muito aquém do esperado", "O serviço foi ruim, não faria novamente",
    "Atendimento ruim, não resolvem o problema", "Serviço demorado e ruim",
    "Foi uma péssima experiência, não recomendo", "A qualidade do serviço foi muito baixa",
    "Atendimento ruim, muito lento", "Fui muito mal atendido, não gostei", "Serviço ruim, poderia ser muito melhor",
    "O trabalho foi insatisfatório", "O atendimento foi horrível, não gostei", "Serviço ruim, totalmente frustrante",
    "Não gostei, foi uma experiência negativa", "O serviço foi muito ruim", "Experiência ruim, muito insatisfeito",
    "Atendimento péssimo, não voltarei", "Serviço mal feito e demorado", "Não recomendo, foi muito ruim",
    "O trabalho foi ruim, poderia ser muito melhor", "O atendimento deixou a desejar", "O serviço foi insatisfatório",
    "Fiquei decepcionado com a qualidade do trabalho", "Foi uma experiência ruim, não voltarei",
    "Não gostei, foi bem abaixo das expectativas", "O atendimento foi muito ruim", "Serviço ruim, nunca mais",
    "A qualidade do serviço foi abaixo do esperado", "Experiência ruim, não me atenderam bem",
    "O trabalho foi péssimo, não atendeu às expectativas", "O atendimento foi de péssima qualidade",
    "Serviço ruim, completamente insatisfeito", "O atendimento foi lento e ineficaz",
    "Serviço mal feito, não voltarei", "O trabalho foi ruim, não volto mais", "Atendimento muito ruim",
    "Serviço muito demorado e ruim", "Péssima experiência, não gostei", "O atendimento foi decepcionante",
    "Serviço ruim, completamente insatisfeito", "O atendimento foi horrível, não gostei",
    "O trabalho foi abaixo do esperado", "A qualidade do serviço foi muito ruim", "Experiência muito ruim",
    "O serviço não valeu a pena", "Atendimento ruim, muito insatisfeito", "Não gostei, foi muito abaixo das expectativas",
    "O trabalho foi mal feito", "Atendimento ruim, totalmente insatisfeito", "Foi uma experiência ruim",
    "Não valeu a pena, serviço péssimo", "Fiquei decepcionado com o serviço", "Foi uma experiência frustrante",
    "O atendimento foi lento e ruim", "Serviço insatisfatório, não volto mais", "O trabalho foi mal feito",
    "A experiência foi ruim, não me senti bem atendido", "O serviço foi péssimo, não gostei",
    "O atendimento foi de péssima qualidade", "Serviço muito ruim", "O atendimento foi totalmente insatisfatório",
    "Serviço péssimo, não valeu a pena", "O atendimento foi completamente insatisfatório",
    "Foi uma experiência negativa, não gostei", "O trabalho foi muito ruim", "O serviço foi muito abaixo da média",
    "O atendimento foi péssimo", "Não gostei, totalmente insatisfeito", "Experiência muito ruim, não volto",
    "O serviço foi muito demorado", "Atendimento ruim, sem paciência", "Serviço abaixo das expectativas",
    "O atendimento foi péssimo, não gostei", "O trabalho foi mal feito, não voltarei", "Serviço ruim",
    "Experiência ruim, péssima", "Não recomendo, atendimento ruim", "O atendimento foi péssimo, não gostei",
    "O serviço foi péssimo", "Atendimento ruim, nada eficiente", "O trabalho foi mal feito",
    "Não gostei, péssimo atendimento", "O serviço foi muito ruim, não retornarei"
]
labels_ruim = ["Ruim"] * len(feedbacks_ruim)

feedbacks_pessimo = [
    "O serviço foi péssimo, não recomendo", "Péssimo atendimento, muito frustrante",
    "Experiência horrível, não voltarei", "O trabalho foi um desastre, não gostei",
    "Serviço de péssima qualidade", "Atendimento péssimo, não quero mais", "Foi uma experiência horrível",
    "Serviço totalmente ineficaz", "O atendimento foi péssimo, demoraram demais",
    "O trabalho foi um pesadelo, não recomendo", "Atendimento insuportável, não gostei",
    "Péssima experiência, não me atenderam direito", "O serviço foi completamente horrível",
    "O atendimento foi desastroso", "Não valeu a pena, péssimo serviço",
    "O serviço foi péssimo, não atendem a demanda", "O atendimento foi de péssima qualidade",
    "Serviço horrível, nunca mais", "Atendimento terrível", "Experiência frustrante, não gostei",
    "Péssimo atendimento, nada resolvem", "O trabalho foi muito ruim", "Não recomendo, serviço péssimo",
    "Foi uma experiência terrível", "O serviço foi um desastre", "Atendimento péssimo", "O serviço não vale a pena",
    "Experiência horrível, péssimo atendimento", "Serviço de qualidade muito baixa", "O atendimento foi completamente falho",
    "O trabalho foi um desastre", "Atendimento desastroso", "Serviço de péssima qualidade",
    "Péssima experiência", "Serviço péssimo, completamente insatisfatório", "Atendimento horrível",
    "Péssimo serviço, não volto mais", "O atendimento foi péssimo", "Péssima experiência, nada de bom",
    "Experiência horrível, péssimo serviço", "Serviço totalmente incompetente", "O atendimento foi terrível",
    "O serviço foi completamente frustrante", "Atendimento péssimo, nada funciona", "Péssimo atendimento",
    "Não gostei, serviço muito ruim", "Péssimo, nem vale a pena", "O serviço foi uma decepção",
    "Atendimento ineficaz", "Serviço terrível", "O atendimento foi desastroso", "Péssima experiência",
    "Serviço foi um desastre", "Atendimento péssimo", "Foi uma decepção, muito ruim",
    "Péssimo serviço, não vale a pena", "Experiência péssima", "Serviço péssimo",
    "Atendimento muito ruim, nada bom", "O serviço foi um pesadelo", "Atendimento sem solução",
    "Péssimo atendimento", "O serviço foi completamente decepcionante", "O atendimento foi péssimo",
    "Serviço ineficaz, não recomendo", "Foi horrível, nunca mais", "O serviço foi péssimo",
    "Atendimento terrível, não gostei", "O trabalho foi mal feito", "Péssima experiência",
    "Experiência péssima, não volto", "Serviço péssimo", "Péssimo atendimento, muito ruim",
    "Serviço de qualidade muito baixa", "Atendimento muito ruim, não voltarei", "O serviço foi terrível"
]
labels_pessimo = ["Péssimo"] * len(feedbacks_pessimo)

# Separando os textos e as classificações
feedbacks = feedbacks_excelente + feedbacks_bom + feedbacks_medio + feedbacks_ruim + feedbacks_pessimo
labels = labels_excellent + labels_bom + labels_medio + labels_ruim + labels_pessimo

# Usando TF-IDF para representar o texto
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(feedbacks)
y = labels

# Treinando o modelo (aqui usamos LogisticRegression, mas você pode trocar para RandomForest ou outro)
model = LogisticRegression()
model.fit(X, y)

# Salvando o modelo treinado
joblib.dump(model, 'feedback_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

app = Flask(__name__)

# Carregar o modelo de machine learning
model = joblib.load('feedback_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Função para obter a conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect('familycare.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rota para receber o feedback e classificar
@app.route('/avaliar_cuidador', methods=['POST'])
def avaliar_cuidador():
    data = request.get_json()

    # Verificar se a requisição contém os dados necessários
    if 'id_idoso' not in data or 'id_cuidador' not in data or 'feedback' not in data:
        return jsonify({'error': 'Dados insuficientes'}), 400

    id_idoso = data['id_idoso']
    id_cuidador = data['id_cuidador']
    feedback = data['feedback']

    # Transformar o feedback com o vectorizer para a representação numérica
    feedback_transformed = vectorizer.transform([feedback])  # Passando como lista de uma lista (2D array)

    # Previsão do modelo sobre o feedback
    classificacao = model.predict(feedback_transformed)[0]

    # Mapeando a classificação para os valores numéricos
    if classificacao == 'Excelente':
        classificacao_num = 5
    elif classificacao == 'Bom':
        classificacao_num = 4
    elif classificacao == 'Médio':
        classificacao_num = 3
    elif classificacao == 'Ruim':
        classificacao_num = 2
    elif classificacao == 'Péssimo':
        classificacao_num = 1

    # Inserir avaliação no banco de dados
    conn = get_db_connection()
    try:
        conn.execute('''INSERT INTO Avaliacoes (id_idoso, id_cuidador, email_idoso, email_cuidador, classificacao, feedback)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                     (id_idoso, id_cuidador, data['email_idoso'], data['email_cuidador'], classificacao_num, feedback))
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify({'message': 'Avaliação registrada com sucesso'}), 200

@app.route('/cuidadores', methods=['GET'])
def listar_cuidadores():
    conn = get_db_connection()
    try:
        # Consultar os cuidadores e suas avaliações
        query = '''
        SELECT c.id, c.nome, AVG(a.classificacao) as media_classificacao
        FROM Cuidadores c
        LEFT JOIN Avaliacoes a ON c.id = a.id_cuidador
        GROUP BY c.id
        ORDER BY media_classificacao DESC
        '''
        cuidadores = conn.execute(query).fetchall()

        # Formatar os resultados em um dicionário para facilitar a conversão para JSON
        resultado = []
        for cuidador in cuidadores:
            resultado.append({
                'id': cuidador['id'],
                'nome': cuidador['nome'],
                'media_classificacao': cuidador['media_classificacao'] if cuidador['media_classificacao'] is not None else 0
            })

        return jsonify(resultado)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)