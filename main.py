import spotipy 
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import os
load_dotenv()

CLIENT_ID =st.secrets['CLIENT_ID']
CLIENT_SECRET =st.secrets['CLIENT_SECRET']
REDIRECT_URI ='http://spotifydashboard-bymarine-journu'

if os.path.exists('.cache'):
    os.remove('.cache')

sp=spotipy.Spotify(    
   auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-top-read user-read-recently-played",
    )
)

st.set_page_config(page_title='Spotify Dashboard', page_icon=':musical_note')
st.title('Spotify Wrap')
st.write('Discover your Spotify listening habits')

top_tracks = sp.current_user_top_tracks(limit=20, time_range='medium_term')

track_data = []
for idx, track in enumerate(top_tracks['items'], start=1):
    track_data.append({
        'Rank': idx,
        'Track Name': track['name'],
        'Artist': ", ".join([artist['name'] for artist in track['artists']]),
        'Album': track['album']['name']
    })

df = pd.DataFrame(track_data)
st.subheader('Your Top 20 Tracks in the past 6 months')
st.table(df)
