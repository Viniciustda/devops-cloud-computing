import os
import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL_PATH = "/model/playlist_rules.pickle"

app.rules = []
app.model_timestamp = 0

def load_model():
    """
    Função auxiliar para carregar/recarregar o modelo do disco
    para a memória da aplicação.
    """
    global app
    print(f"Attempting to load model from {MODEL_PATH}...")
    try:
        with open(MODEL_PATH, 'rb') as f:
            app.rules = pickle.load(f)
            app.model_timestamp = os.path.getmtime(MODEL_PATH)
        print(f"Successfully loaded {len(app.rules)} rules. New timestamp: {app.model_timestamp}")
    except FileNotFoundError:
        print(f"Model file not found at {MODEL_PATH}. Ruleset remains empty.")
        app.rules = []
        app.model_timestamp = 0
    except Exception as e:
        print(f"An error occurred loading model: {e}")
        app.rules = []
        app.model_timestamp = 0

load_model()

@app.route("/api/recommend", methods=["POST"])
def recommend():
    global app 
    
    try:
        current_timestamp = os.path.getmtime(MODEL_PATH)
        
        if current_timestamp > app.model_timestamp:
            print("New model file detected! Reloading rules...")
            load_model()
            
    except FileNotFoundError:
        pass 
        
    if not request.json or 'songs' not in request.json:
        return jsonify({"error": "Request must be JSON with a 'songs' key"}), 400

    input_songs = request.json['songs']
    input_song_set = set(input_songs)

    recommendations = set()
    for rule in app.rules:
        antecedent = rule[0]
        consequent = rule[1]
        
        if antecedent.issubset(input_song_set) and not consequent.issubset(input_song_set):
            recommendations.update(consequent)

    response_data = {
        "songs": list(recommendations),
        "version": "2.1", 
        "model_date": app.model_timestamp 
    }
    
    return jsonify(response_data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 50031))
    app.run(host='0.0.0.0', port=port, debug=False)