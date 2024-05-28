import streamlit as st
from pymongo import MongoClient
import pandas as pd
import json
import re

# Config
client = MongoClient("mongodb://localhost:27017/")
db = client["datasets"]

# Titre de l'application
st.title("Application de Gestion des Fichiers et Recherches MongoDB")

# Charger un fichier
uploaded_file = st.file_uploader("Choisir un fichier", type=["csv", "json"])

if uploaded_file is not None:
    
    collection_name = re.sub(r'[\s-]', '_', uploaded_file.name.split('.')[0])
    
    # Lire le fichier en fonction de son type
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.json'):
        data = pd.read_json(uploaded_file)
    
    # Convertir le dataframe en dictionnaire et insérer dans la collection MongoDB
    collection = db[collection_name]
    collection.insert_many(data.to_dict('records'))
    
    st.success(f"Fichier {uploaded_file.name} chargé avec succès dans la collection '{collection_name}'.")

# Afficher les collections disponibles
collections = db.list_collection_names()
selected_collection = st.selectbox("Choisir une collection", collections)

# Champ de texte pour le critère de recherche
search_criteria = st.text_area("Saisir le critère de recherche (au format JSON)", "{}")

# Bouton pour effectuer la recherche
if st.button("Rechercher"):
    try:
        # Convertir le critère de recherche en dictionnaire
        search_criteria_dict = json.loads(search_criteria)
        
        # Effectuer la recherche
        collection = db[selected_collection]
        results = collection.find(search_criteria_dict)
        
        # Convertir les résultats en dataframe et les afficher
        results_df = pd.DataFrame(list(results))
        if not results_df.empty:
            st.dataframe(results_df)
        else:
            st.write("Aucun résultat trouvé.")
    except Exception as e:
        st.error(f"Erreur lors de la recherche : {e}")





