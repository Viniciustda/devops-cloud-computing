import os
import pickle
from flask import Flask, request, jsonify

# Inicialização do Flask
app = Flask(__name__)

# Carrega o modelo de regras
# Define o caminho onde o modelo ficará no Kubernetes
# Este caminho será criado a partir do Persistent Volume
MODEL_PATH = "/model/playlist_rules.pickle"

print(f"Loading model from {MODEL_PATH}...")
try:
    with open(MODEL_PATH, 'rb') as f:
        # Carrega as regras para a memória
        app.rules = pickle.load(f)
    print(f"Successfully loaded {len(app.rules)} rules.")
except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_PATH}")
    print("Please run 'generate_rules.py' first to create the model file.")
    app.rules = [] # Inicia com regras vazias se o arquivo não for encontrado


# Define o Endpoint da API
# @app.route define a URL: /api/recommend
# methods=["POST"] significa que esta URL só aceita requisições do tipo POST
@app.route("/api/recommend", methods=["POST"])
def recommend():
    """
    Espera um JSON no corpo da requisição com a chave "songs".
    Ex: {"songs": ["Yesterday", "Bohemian Rhapsody"]}
    
    Retorna um JSON com as músicas recomendadas.
    Ex: {"songs": ["..."], "version": "0.1", "model_date": "..."}
    """
    print("Received request on /api/recommend")

    # Validaa a requisição 
    if not request.json or 'songs' not in request.json:
        print("Error: Request is not valid JSON or 'songs' key is missing.")
        return jsonify({"error": "Request must be JSON with a 'songs' key"}), 400

    input_songs = request.json['songs']
    input_song_set = set(input_songs)

    # Lógica de recomendação simples
    recommendations = set()
    for rule in app.rules:
        antecedent = rule[0]
        consequent = rule[1]
        
        if antecedent.issubset(input_song_set) and not consequent.issubset(input_song_set):
            recommendations.update(consequent)

    # Formata a Resposta
    
    model_timestamp = 0 # Define um timestamp padrão (0)
    try:
        # Tenta pegar a data de modificação do arquivo de regras
        model_timestamp = os.path.getmtime(MODEL_PATH)
    except FileNotFoundError:
        # Se o arquivo não existir, apenas continua com o timestamp 0
        print("Model file not yet available for timestamp.")
        pass

    response_data = {
        "songs": list(recommendations),
        "version": "1.0", 
        "model_date": model_timestamp
    }
    
    print(f"Responding with {len(recommendations)} recommendations.")
    return jsonify(response_data)

# Executa o servidor
if __name__ == '__main__':
    # Define a porta do usuário
    port = int(os.environ.get("PORT", 50031))
    
    # 0.0.0.0 aceita conexões de qualquer IP 
    app.run(host='0.0.0.0', port=port, debug=False)