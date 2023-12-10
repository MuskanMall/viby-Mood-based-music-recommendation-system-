import json
import base64
from requests import post, get
import os

CLIENT_ID = 'e656fd8e62c94898ba2e63e50a95b37a'
CLIENT_SECRET = '41244b13adb445839858f8241166e15c'
REDIRECT_URI = 'http://localhost/'
USER_ID = "31fblw4yma7uvm626hujymggbu6a"

Artist_uris = []
ALBUMS = {}
TRACKS = {}
TRACK_FEATURES = {}

MOOD_RANGES = {
    "sad": (0.0, 0.49),
    "neutral": (0.49, 0.74),
    "happy": (0.75, 1.0),
}

'''Sad mood, the range is [0.0 to 0.09], for Angry mood, [0.10 to 0.24], for disgust or fear mood, the range is [0.25 
to 0.49], for neutral mood, the range is [0.49 to 0.74], for surprised mood, the range is [0.75 to 0.89] and for 
happy mood, the range is [0.90 to 1.00]'''

'''
if the mood detected is suprised or happy then go with happy playlist 
if the mood detected is sad or angry or fear then go with sad playlist
'''


# GETTING THE TOKEN FROM SPOTIFY
def get_token():
    authorization = base64.b64encode(bytes(f'{CLIENT_ID}:{CLIENT_SECRET}', 'utf-8')).decode('utf-8')
    url = "https://accounts.spotify.com/api/token"
    header = {
        "authorization": f"Basic {authorization}",
        "content-type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    # SENDING A POST-REQUEST TO SPOTIFY, TO GET THE TOKEN
    response = post(url, headers=header, data=data)
    # EXTRACTING THE TOKEN FROM THE RESPONSE
    json_response = json.loads(response.content)
    # CONVERTING IT INTO PYTHON DICTIONARY
    token = json_response['access_token']

    return token


def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}


# ARTIST-BASED MUSIC EXTRACTION
def get_artist_uri(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    header = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=50"
    response = get(url, headers=header, params=query)
    json_response = json.loads(response.content)['artists']['items']
    if len(json_response) == 0:
        print("Invalid artist name")
        return None
    else:
        return json_response[0]['id']


def get_artist_top_albums(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    header = get_auth_header(token)
    query = "include_groups=album&limit=50"
    response = get(url, headers=header, params=query)
    json_response = json.loads(response.content)['items']
    if len(json_response) == 0:
        print("No albums found for the artist")
        return None
    else:
        ALBUMS.update({album['uri']: album['name'] for album in json_response})
        return ALBUMS


def classify_songs_on_mood(mood):
    if mood == 'angry' or mood == 'fear' or mood == 'disgust':
        mood = 'sad'
    if mood == 'surprised':
        mood = 'happy'
    PLAYLIST_BASED_ON_MOOD = []
    mood_range = MOOD_RANGES.get(mood)
    if mood_range is None:
        raise Exception("Invalid mood")
    for track_info in TRACK_FEATURES.values():
        uri = track_info['uri']
        valence = track_info['valence']
        if mood_range[0] <= valence <= mood_range[1]:
            PLAYLIST_BASED_ON_MOOD.append(uri)

    return PLAYLIST_BASED_ON_MOOD


def get_tracks_from_album(token, album_ids):
    for album_id in album_ids:
        album_id = album_id[14:]
        url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
        header = get_auth_header(token)
        query = f"q=limit=20"
        response = get(url, headers=header, params=query)
        json_response = json.loads(response.content)['items']
        if len(json_response) == 0:
            print("No tracks found for the album")
        else:
            TRACKS.update({track['uri']: track['name'] for track in json_response})


def _helper_get_track_features(token, track_ids):
    url = "https://api.spotify.com/v1/audio-features"
    header = get_auth_header(token)
    params = {"ids": ",".join(track_ids)}
    response = get(url, headers=header, params=params)
    json_response = json.loads(response.content)

    for track_feature in json_response['audio_features']:
        if track_feature:
            track_id = track_feature['id']
            TRACK_FEATURES[track_id] = {key: track_feature[key] for key in ['valence', 'uri', 'track_href']}


def get_track_features(token, tracks):
    batch_size = 50  # Spotify allows up to 100 tracks per request, adjust as needed
    for i in range(0, len(tracks), batch_size):
        batch = tracks[i:i + batch_size]
        track_ids = [track[14:] for track in batch]  # Extracting the ID from the URIs
        _helper_get_track_features(token, track_ids)


def get_song_list(artist_name, mood):
    token = get_token()
    artist_uri = get_artist_uri(token, artist_name)
    if artist_uri is None:
        raise Exception("Invalid artist name")
    get_artist_top_albums(token, artist_uri)
    get_tracks_from_album(token, list(ALBUMS.keys()))
    get_track_features(token, list(TRACKS.keys()))
    playlist = classify_songs_on_mood(mood)
    return playlist



