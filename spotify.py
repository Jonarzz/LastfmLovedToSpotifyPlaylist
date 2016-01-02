import spotipy
import my_spotipy.util as util

import lastfm

import properties

__author__ = 'Jonarzz'


class TokenGenerationException(Exception):
    pass


def generate_token(spotify_username):
    token = util.prompt_for_user_token(spotify_username, properties.MODIFY_PLAYLISTS_SCOPE,
                                       properties.SPOTIFY_API_ID, properties.SPOTIFY_API_SECRET,
                                       properties.SPOTIFY_REDIRECT_URL)
    if token:
        return token
    else:
        raise TokenGenerationException('Could not generate token.')


def create_spotify_object(token):
    spotify = spotipy.Spotify(auth=token)
    spotify.trace = False
    return spotify


def create_spotify_tracks_ids_list_from_loved(loved_tracks, spotify):
    tracks_ids = []
    number_of_loved_tracks = len(loved_tracks)
    done_tracks = 0

    for track in loved_tracks:
        done_tracks += 1
        print_progress(done_tracks, number_of_loved_tracks)

        search_query = create_search_query(track)

        id = get_track_id_from_search_query(spotify, search_query, track['artist'])
        if id:
            tracks_ids.append(id)

    return tracks_ids


def create_playlist_for_user(spotify, spotify_username, playlist_name):
    playlist = spotify.user_playlist_create(spotify_username, playlist_name)
    return playlist['id']


def add_tracks_to_playlist(spotify, spotify_username, playlist_id, tracks_ids, tracks_per_requests=100):
    for tracks_chunk in [tracks_ids[i:i + tracks_per_requests] for i in
                         range(0, len(tracks_ids), tracks_per_requests)]:
        spotify.user_playlist_add_tracks(spotify_username, playlist_id, tracks_chunk)


def print_progress(done_tracks, number_of_loved_tracks):
    print('{0:.2f}%'.format(done_tracks / number_of_loved_tracks * 100))


def create_search_query(track):
    title = track['title']

    for ending in properties.TITLE_ENDINGS_TO_CUT:
        if title.find(ending) != -1:
            title = title[:title.find(ending)]

    return track['artist'] + ' ' + title


def get_track_id_from_search_query(spotify, search_query, artist_name):
    results = spotify.search(search_query)

    try:
        for item in results['tracks']['items']:
            if item['artists'][0]['name'] == artist_name:
                return item['id']

        return results['tracks']['items'][0]['id']
    except IndexError:
        return None
