import os
import spotipy

from spotipy.oauth2 import SpotifyOAuth

def authenticate_spotify():
    
    spotify_client_id = os.getenv(
        "SPOTIFY_CLIENT_ID"
    )  
    spotify_client_secret = os.getenv(
        "SPOTIFY_CLIENT_SECRET"
    )  
    spotify_redirect_url = os.getenv(
        "SPOTIFY_REDIRECT_URL"
    )  

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=spotify_client_id,
            client_secret=spotify_client_secret,
            redirect_uri=spotify_redirect_url,
            scope="user-read-recently-played",
        )
    )
    recently_played = sp.current_user_recently_played(limit=50)
    
    return recently_played
        