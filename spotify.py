"""Module used to wrap the spotipy module using Spotify API in order to connect to Spotify,
authorize, create a playlist for given user and add tracks from a given list with track IDs
to the playlist."""

import spotipy

import my_spotipy.util as util
import properties

__author__ = 'Jonarzz'


class TokenGenerationException(Exception):
    """Exception raised when token generation fails
    (e.g. wrong username, no access granted from the user)."""
    pass


def generate_token():
    """Method that returns a spotipy Spotify API token for a given username, if the user
    gave the permission to connect the app with their account.
    If the token could not be generated, TokenGenerationException is raised."""
    return util.prompt_for_user_token(properties.MODIFY_PLAYLISTS_SCOPE,
                                       properties.SPOTIFY_API_ID,
                                       properties.SPOTIFY_API_SECRET,
                                       properties.SPOTIFY_REDIRECT_URL)


def create_spotify_object(token):
    """Method that returns a spotipy.Spotify object created using given token."""
    spotify_obj = spotipy.Spotify(auth=token)
    spotify_obj.trace = False
    return spotify_obj


def create_spotify_tracks_ids_list_from_loved(loved_tracks, spotify_obj):
    """Method that returns a list of Spotify tracks IDs for a given LastFM loved_tracks
    dictionaries list and authorized spotipy.Spotify object. Prints progress of creation
    the list in percents to the console."""
    tracks_ids = []
    number_of_loved_tracks = len(loved_tracks)
    done_tracks = 0

    for track in loved_tracks:
        done_tracks += 1
        calculate_progress(done_tracks, number_of_loved_tracks, print_progress=True)

        search_query = create_search_query(track)

        track_id = get_track_id_from_search_query(spotify_obj, search_query, track['artist'])
        if track_id:
            tracks_ids.append(track_id)

    return tracks_ids


def create_playlist_for_user(spotify_obj, spotify_username, playlist_name):
    """Method that creates a playlist with given name for given username, using authorized
    spotipy.Spotify object. Created playlist ID is returned."""
    playlist = spotify_obj.user_playlist_create(spotify_username, playlist_name)
    return playlist['id']


def add_tracks_to_playlist(spotify_obj, spotify_username, playlist_id, tracks_ids,
                           tracks_per_requests=100):
    """Method that adds tracks with given Spotify tracks IDs to Spotify user's playlist
    with a given playlist ID. Spotipy.Spotify object is used to add the tracks.
    Maximum tracks per request in Spotify API is 100 and the same number is set in the method
    by default. Can be changed to a number below 100."""
    results = []
    for tracks_chunk in [tracks_ids[i:i + tracks_per_requests] for i in
                         range(0, len(tracks_ids), tracks_per_requests)]:
        results.append(spotify_obj.user_playlist_add_tracks(spotify_username,
                                                        playlist_id,
                                                        tracks_chunk))
    return results


def calculate_progress(done_tracks, number_of_loved_tracks, print_progress=False):
    """Method that calculates and may print (changeable by print argument, False by default)
    progress of list creation in XX.XX% format."""
    output = '{0:.2f}%'.format(done_tracks / number_of_loved_tracks * 100)
    if print_progress:
        print(output)

    return output


def create_search_query(track):
    """Method that can be used to create a search query passed to the Spotify API.
    The track argument is a dictionary in such format:
    {'artist': artist-name, 'title': track-title}"""
    artist = track['artist']
    title = track['title']

    for ending in properties.TITLE_ENDINGS_TO_CUT:
        if title.find(ending) != -1:
            title = title[:title.find(ending)]

    artist = artist.strip()
    title = title.strip()

    return artist + ' ' + title


def get_track_id_from_search_query(spotify_obj, search_query, artist_name):
    """Method that returns a track ID returned from the search using Spotify API
    (managed by spotipy.Spotify object passed to the method) for a given search query
    and expected artist name (or the first result's ID, if the name was not found)."""
    results = spotify_obj.search(search_query)

    try:
        for item in results['tracks']['items']:
            if item['artists'][0]['name'] == artist_name:
                return item['id']

        return results['tracks']['items'][0]['id']
    except IndexError:
        return None
