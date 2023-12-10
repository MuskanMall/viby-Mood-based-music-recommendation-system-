import random

from spotify_playlist_creation import create_playlist_and_add_songs
from spotify_utils import get_song_list


def get_playlist_url(artists, mood):
    song_uris = []
    for artist in artists:
        song_uris += get_song_list(artist, mood)
    if len(song_uris) > 30:
        song_uris = random.sample(song_uris, 30)
    playlist_url = create_playlist_and_add_songs(playlist_name=f'Viby: Music for your mood- {mood}', song_uris=song_uris)
    if playlist_url is None:
        raise Exception("Invalid playlist name")

    return playlist_url


# print(get_playlist_url(['J Cole', 'Sampa the great'], 'sad'))









# import json
# import base64
# from requests import post, get
# # import spotify_utils as helper
# import os
# import spotipy

# # set the env file path
# from dotenv import load_dotenv
# from spotipy.oauth2 import SpotifyOAuth
# load_dotenv()

# #get client id and secret from env file
# CLIENT_ID = os.getenv("CLIENT_ID")
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# REDIRECT_URI = os.getenv("REDIRECT_URI")
# USER_ID = os.getenv("USER_ID")
# SCOPE = "playlist-modify-public playlist-modify-private"

# def get_spotify_client():
#     # ESTABLISHING CONNECTION WITH SPOTIFY LIBRARY
#     sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
#                                                    client_secret=CLIENT_SECRET,
#                                                    redirect_uri=REDIRECT_URI,
#                                                    scope=SCOPE))

#     return sp

# print(get_spotify_client())


# # GETTING THE TOKEN FROM SPOTIFY
# def get_token():
#     authorization = base64.b64encode(bytes(f'{CLIENT_ID}:{CLIENT_SECRET}', 'utf-8')).decode('utf-8')
#     url = "https://accounts.spotify.com/api/token"
#     header = {
#         "authorization": f"Basic {authorization}",
#         "content-type": "application/x-www-form-urlencoded"
#     }
#     data = {"grant_type": "client_credentials"}
#     # SENDING A POST-REQUEST TO SPOTIFY, TO GET THE TOKEN
#     response = post(url, headers=header, data=data)
#     # EXTRACTING THE TOKEN FROM THE RESPONSE
#     json_response = json.loads(response.content)
#     # CONVERTING IT INTO PYTHON DICTIONARY
#     token = json_response['access_token']

#     return token


# token = get_token()

# helper.get_song_list(token,"Sampa the great")
