# Sistema de Recomendação de Cuidadores para Idosos

## Objetivo do Programa
O programa desenvolvido tem como objetivo recomendar cuidadores ideais para idosos com base em um conjunto de características e condições. Utilizando um algoritmo de aprendizado de máquina, o sistema analisa as necessidades e as condições dos idosos e escolhe o cuidador mais adequado, levando em consideração características como mobilidade, obesidade, deficiência, dificuldades visuais, auditivas e condições médicas.

O sistema também permite que o usuário escolha um idoso específico para o qual será feita a recomendação personalizada de um cuidador.

## Estrutura e Fluxo do Programa

### 1. Carregamento de Dados
O sistema começa carregando dados do banco de dados SQLite (`familycare.db`), onde estão armazenadas informações sobre os idosos e cuidadores. Essas informações incluem características relevantes, como:

- **Idosos**: Nome, mobilidade, obesidade, deficiência, dificuldades visuais, auditivas e condições médicas.
- **Cuidadores**: Nome, habilidades e características de cuidados em relação às mesmas condições dos idosos.

**Função**: `carregar_dados()`
- Carrega os dados das tabelas `Idosos` e `Cuidadores` do banco de dados e os converte em DataFrames do Pandas para processamento posterior.

### 2. Recomendação de Cuidador
Quando um idoso é selecionado, o programa utiliza um algoritmo de k-Nearest Neighbors (kNN) para encontrar o cuidador mais adequado, comparando as características do idoso com aquelas dos cuidadores.

**Função**: `recomendar_cuidador(idoso_dados, cuidadores_df)`
- Codifica as características dos cuidadores e do idoso selecionado em variáveis numéricas, usando a técnica de *one-hot encoding* (ou codificação binária).
- Aplica o algoritmo de kNN para encontrar o cuidador que mais se assemelha ao idoso, ou seja, o cuidador cujas características são mais próximas (no espaço vetorial) das do idoso.
- O kNN retorna o cuidador mais próximo baseado nas características codificadas.

### 3. Interface com o Usuário
Através de um menu interativo, o programa solicita que o usuário escolha um idoso do banco de dados. Após a escolha, o sistema recomenda o cuidador mais adequado, exibindo o nome do cuidador ideal para aquele idoso.

**Função**: `exibir_menu_de_idosos()`
- Exibe uma lista numerada de idosos cadastrados e pede ao usuário para selecionar um deles.
- Após a escolha, a recomendação do cuidador é feita com base nas características do idoso selecionado.

### 4. Execução do Programa
O programa principal é a função `realizar_matching()`, que orquestra o fluxo de carregamento dos dados, seleção do idoso e recomendação do cuidador.

## Como o Algoritmo Funciona

### 1. Codificação dos Dados
Para garantir que os dados possam ser processados pelo modelo de aprendizado de máquina, as variáveis categóricas (como "Sim" ou "Não") são convertidas em variáveis numéricas. A codificação é feita utilizando o `pd.get_dummies()`, uma técnica comum para transformar variáveis categóricas em uma forma numérica, onde cada categoria é representada por uma coluna separada, com valores binários (0 ou 1).

**Exemplo**:
- Se um idoso possui a condição de mobilidade, a coluna "mobilidade" será codificada como 1, caso contrário, será 0.

### 2. Algoritmo k-Nearest Neighbors (kNN)
O algoritmo escolhido para a recomendação dos cuidadores foi o k-Nearest Neighbors. Esse algoritmo funciona encontrando os vizinhos mais próximos de um ponto de dados em um espaço vetorial. No contexto deste sistema:
- Cada cuidador e idoso são representados como pontos em um espaço multidimensional, onde cada dimensão corresponde a uma característica (como mobilidade, deficiência, etc.).
- O kNN compara as distâncias entre o ponto representando o idoso e todos os pontos dos cuidadores. O cuidador mais próximo (com a menor distância) é o recomendado.

### Por que kNN foi escolhido?
O kNN é um algoritmo simples, eficaz e amplamente utilizado para problemas de recomendação e classificação. Ele é intuitivo e fácil de implementar, além de não exigir um treinamento complexo. Para o caso específico de recomendação de cuidadores para idosos, o kNN é uma escolha apropriada, pois os dados são relativamente pequenos e não exigem técnicas mais complexas, como redes neurais. Além disso, a ideia de encontrar o "vizinho mais próximo" (o cuidador mais adequado) faz sentido dentro do contexto de características semelhantes.

O kNN é especialmente útil quando não há uma relação linear clara entre as variáveis de entrada, como no caso de características como "mobilidade", "deficiência", "obesidade", etc. O algoritmo pode capturar essas complexidades de maneira eficaz.

## Busca pelo Cuidador Ideal
Quando um idoso é selecionado, o sistema realiza a codificação de suas características, alinha os dados entre o idoso e os cuidadores (para garantir que ambos tenham o mesmo formato de dados) e, em seguida, utiliza o kNN para calcular a "distância" entre o idoso e todos os cuidadores. O cuidador com a menor distância é selecionado como a recomendação.

## Escolha do Algoritmo
O k-Nearest Neighbors (kNN) foi escolhido por algumas razões principais:
- **Simplicidade e Eficiência**: O kNN é fácil de entender e implementar. Como o programa não precisa de um modelo complexo, a escolha por um algoritmo simples e direto faz mais sentido.
- **Recomendação baseada em características**: O kNN é adequado para problemas de recomendação em que as variáveis podem ser tratadas como um vetor de características (como no caso de idosos e cuidadores).
- **Sem necessidade de treinamento prévio**: O kNN não requer treinamento, o que significa que o sistema pode ser atualizado facilmente com novos dados, sem a necessidade de retreinar o modelo.

Apesar de ser simples, o kNN é poderoso para encontrar padrões em conjuntos de dados pequenos e médios, como o conjunto de dados de cuidadores e idosos usado aqui. Caso o banco de dados cresça muito no futuro, seria possível explorar algoritmos mais avançados, como redes neurais ou árvores de decisão, mas o kNN ainda seria uma escolha viável para o problema atual.

## Considerações Finais
Este sistema de recomendação foi projetado para fornecer uma solução prática e simples para conectar idosos a cuidadores adequados. A escolha do algoritmo kNN foi motivada pela simplicidade e eficácia para o problema específico, onde as relações entre as variáveis não precisam ser modeladas de forma muito complexa.

No futuro, o sistema pode ser expandido para incluir mais variáveis de entrada, realizar análises mais profundas dos dados, ou até mesmo utilizar algoritmos mais avançados conforme o número de dados aumenta.

Este programa, embora simples, pode oferecer uma base robusta para o desenvolvimento de um sistema de recomendação de cuidadores, ajudando a otimizar a assistência aos idosos com base nas suas necessidades específicas.
