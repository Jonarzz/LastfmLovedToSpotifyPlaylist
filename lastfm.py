"""Module that uses LastFM API. Establishes connection with LastFM and allows to get loved tracks
for a given user."""

import pylast

import properties

__author__ = 'Jonarzz'


def get_loved_tracks(username, password):
    """Method that returns a list of track dictionaries in such format:
    {'artist': artist-name, 'title': track-title}
    for the user with given username and password."""
    loved_tracks = get_lastfm_user(username, password).get_loved_tracks(limit=None)

    tracks_list = []
    for loved_track in loved_tracks:
        track = {'artist': loved_track.track.artist.get_name(),
                 'title': loved_track.track.title}
        tracks_list.append(track)

    return tracks_list


def get_lastfm_user(username, password):
    """Method that establishes connection to the LastFM API with key and secret provided
    in the properties file. After the successful connection, User object is returned."""
    password_hash = pylast.md5(password)
    network = pylast.LastFMNetwork(
        api_key=properties.API_KEY, api_secret=properties.API_SECRET,
        username=username, password_hash=password_hash)

    return network.get_user(username)
