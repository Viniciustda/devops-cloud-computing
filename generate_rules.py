import pandas as pd
import pickle
from fpgrowth_py import fpgrowth
import os

print("Starting rule generation (ML Container)...")

# Carrega o dataset 
default_path = '/home/datasets/spotify/2023_spotify_ds1.csv'
dataset_path = os.environ.get('DATASET_PATH', default_path)

print(f"Loading dataset from: {dataset_path}")

try:
    df = pd.read_csv(dataset_path, usecols=['pid', 'track_name'])
except FileNotFoundError:
    print(f"Error: Dataset file not found at {dataset_path}")
    exit()

print("Dataset loaded. Processing transactions...")

# Processa transações (Agrupa músicas por playlist)
transactions = df.groupby('pid')['track_name'].apply(list)
itemSetList = transactions.tolist()
print(f"Total of {len(itemSetList)} playlists (transactions) processed.")

# Roda o Algoritmo FP-Growth
min_support = 0.05
min_confidence = 0.1
print(f"Running FP-Growth with support={min_support} and confidence={min_confidence}...")

freqItemSet, rules = fpgrowth(itemSetList, minSupRatio=min_support, minConf=min_confidence)
print(f"Generation complete. {len(rules)} rules found.")

# Salva o Modelo
model_path = "/model/playlist_rules.pickle"

print(f"Saving rules to shared volume: {model_path}")

try:
    with open(model_path, 'wb') as f:
        pickle.dump(rules, f)
    print("Model saved successfully!")
    print("Script 'generate_rules.py' finished.")

except FileNotFoundError:
    print(f"Error: Could not write to {model_path}.")
    print("This container must be run with a volume mounted at /model/")
    exit(1)