"""Module that uses LastFM API. Establishes connection with LastFM and allows to get loved tracks
for a given user."""

import pylast

import properties

__author__ = 'Jonarzz'


class WrongCredentialsException(Exception):
    """Exception raised when LastFM username and password do pass the verification."""
    pass


def get_loved_tracks_list(user):
    """Method that returns a list of track dictionaries in such format:
    {'artist': artist-name, 'title': track-title}
    for the given user."""
    return [create_track_dict(loved_track) for loved_track in get_loved_tracks(user)]


def create_track_dict(loved_track):
    """Method that creates a dictionary for a given LovedTrack object from LastFM API
    in such format:
    {'artist': artist-name, 'title': track-title}"""
    return {'artist': loved_track.track.artist.get_name(),
            'title': loved_track.track.title}


def get_loved_tracks(user, track_limit=None):
    """Method that returns pylast.LovedTrack objects using LastFM API."""
    return user.get_loved_tracks(limit=track_limit)


def get_lastfm_user(username, password):
    """Method that establishes connection to the LastFM API with key and secret provided
    in the properties file. After the successful connection, User object is returned.
    If the username and password do not match, WrongCredentialsException is raised."""
    password_hash = pylast.md5(password)

    try:
        network = pylast.LastFMNetwork(
            api_key=properties.LASTFM_API_KEY, api_secret=properties.LASTFM_API_SECRET,
            username=username, password_hash=password_hash)
    except pylast.WSError:
        raise WrongCredentialsException

    return network.get_user(username)
