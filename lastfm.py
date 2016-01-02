"""Module that uses LastFM API. Establishes connection with LastFM and allows to get loved tracks
for a given user."""

import pylast

import properties

__author__ = 'Jonarzz'


def get_loved_tracks_list(username, password):
    """Method that returns a list of track dictionaries in such format:
    {'artist': artist-name, 'title': track-title}
    for the user with given username and password."""
    return [create_track_dict(loved_track) for loved_track in get_loved_tracks(username, password)]


def create_track_dict(loved_track):
    """Method that creates a dictionary for a given loved_track from LastFM API in such format:
    {'artist': artist-name, 'title': track-title}"""
    return {'artist': loved_track.track.artist.get_name(),
            'title': loved_track.track.title}


def get_loved_tracks(username, password, track_limit=None):
    """Method that returns loved tracks objects using LastFM API."""
    return get_lastfm_user(username, password).get_loved_tracks(limit=track_limit)


def get_lastfm_user(username, password):
    """Method that establishes connection to the LastFM API with key and secret provided
    in the properties file. After the successful connection, User object is returned."""
    password_hash = pylast.md5(password)
    network = pylast.LastFMNetwork(
        api_key=properties.API_KEY, api_secret=properties.API_SECRET,
        username=username, password_hash=password_hash)

    return network.get_user(username)
