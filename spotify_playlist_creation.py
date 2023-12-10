import os
import spotipy

from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = '31a42b2cd2de4fc4b6b4cbfe22d22afc'
CLIENT_SECRET = '857ad77cfec948a38fc022d187fa72ad'
REDIRECT_URI = 'http://localhost/'


SCOPE = "playlist-modify-public playlist-modify-private"



# song_uris = [uri.split(':')[-1] for uri in song_uris]
# print(song_uris)
def get_spotify_client():
    # ESTABLISHING CONNECTION WITH SPOTIFY LIBRARY
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri=REDIRECT_URI,
                                                   scope=SCOPE))

    return sp


def get_playlist_url(playlist_uri):
    playlist_id = playlist_uri.split(':')[-1]  # Extract the playlist ID from the URI
    playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"
    return playlist_url


def create_playlist_and_add_songs(playlist_name, song_uris):
    sp = get_spotify_client()
    # Create a new playlist
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True)

    song = '2YIIDMcF9zWJ2xcFSA99lH'
    # Add songs to the playlist using their URIs

    sp.playlist_add_items(playlist['id'], song_uris)

    # Return the playlist URI
    return get_playlist_url(playlist['uri'])

# print(get_spotify_client())


