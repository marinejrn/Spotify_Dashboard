import spotipy 
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import os


# Charger les variables d'environnement
load_dotenv()
if os.path.exists('.cache'):
    os.remove('.cache')
# Récupérer les secrets API
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = "http://localhost:3000"

# Initialisation de l'authentification Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-top-read"
))

# Configuration de la page Streamlit
st.set_page_config(page_title="Spotify Dashboard", page_icon=":musical_note:")
st.title("Spotify Dashboard 🎧")
st.write("Explorez vos habitudes d'écoute sur différentes périodes.")

# Options de temps pour l'utilisateur
time_range_options = {
    "4 dernières semaines": "short_term",
    "6 derniers mois": "medium_term",
    "Long terme (plusieurs années)": "long_term"
}

# Ajout d'un sélecteur pour le choix de la période
selected_time_range = st.selectbox(
    "Choisissez la période d'analyse :",
    options=list(time_range_options.keys())
)

# Récupérer la clé correspondante pour l'API Spotify
api_time_range = time_range_options[selected_time_range]

# Récupération des morceaux les plus écoutés selon la période sélectionnée
top_tracks = sp.current_user_top_tracks(limit=20, time_range=api_time_range)

# Préparer les données pour l'affichage
track_data = []
for idx, track in enumerate(top_tracks['items'], start=1):
    track_data.append({
        "Rang": idx,
        "Nom du morceau": track["name"],
        "Artiste": ", ".join([artist["name"] for artist in track["artists"]]),
        "Album": track["album"]["name"]
    })

# Convertir en DataFrame
df = pd.DataFrame(track_data)

# Afficher les résultats
st.subheader(f"Vos morceaux les plus écoutés : {selected_time_range}")
st.table(df)
