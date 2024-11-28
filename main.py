import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

# Configuration de l'application Spotify
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
REDIRECT_URI = "https://spotifydashboard-bymarine-journu.streamlit.app"
scope = "user-top-read user-read-recently-played"

# Titre de l'application
st.title("Spotify Wrap")
st.write("Discover your Spotify listening habits")

# Gestion de l'autorisation avec session_state
if "auth_manager" not in st.session_state:
    st.session_state["auth_manager"] = None

if st.session_state["auth_manager"] is None:
    # Étape 1 : Initialiser l'OAuth
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=scope,
        open_browser=False
    )
    auth_url = auth_manager.get_authorize_url()
    st.write("1. [Cliquez ici pour vous connecter à Spotify](%s)" % auth_url)
    st.write("2. Copiez l'URL vers laquelle vous êtes redirigé, puis collez-la ci-dessous.")

    # Étape 2 : Entrer l'URL de redirection
    redirect_response = st.text_input("Entrez l'URL de redirection ici")
    if redirect_response:
        try:
            st.session_state["auth_manager"] = auth_manager.get_access_token(redirect_response)
            st.experimental_rerun()
        except Exception as e:
            st.error("Erreur lors de l'autorisation. Veuillez réessayer.")
else:
    # Utilisateur connecté, afficher les données Spotify
    sp = spotipy.Spotify(auth=st.session_state["auth_manager"]["access_token"])

    # Récupérer les morceaux les plus écoutés
    top_tracks = sp.current_user_top_tracks(limit=10, time_range='medium_term')
    data = []
    for idx, track in enumerate(top_tracks["items"], start=1):
        data.append({
            "Rank": idx,
            "Track Name": track["name"],
            "Artist": ", ".join([artist["name"] for artist in track["artists"]]),
            "Album": track["album"]["name"]
        })

    # Convertir en DataFrame et afficher
    df = pd.DataFrame(data)
    st.subheader("Your Top 10 Tracks")
    st.table(df)
