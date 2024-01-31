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


