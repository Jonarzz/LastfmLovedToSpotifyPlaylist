"""Main module of the LastfmLovedToSpotifyPlaylist project."""

import sys

import lastfm
import spotify

__author__ = 'Jonasz'


def lastfm_fav_to_spotify_playlist():
    """Main method of the module and project that brings together other modules using APIs."""
    loved_tracks, spotify_username, playlist_name = extract_variables()

    try:
        token = spotify.generate_token(spotify_username)
    except spotify.TokenGenerationException:
        print('Error generating token.')  # GUI => dialog window
    else:
        sp = spotify.create_spotify_object(token)
        tracks_ids = spotify.create_spotify_tracks_ids_list_from_loved(loved_tracks, sp)
        playlist_id = spotify.create_playlist_for_user(sp, spotify_username, playlist_name)
        spotify.add_tracks_to_playlist(sp, spotify_username, playlist_id, tracks_ids)


def extract_variables():
    try:
        lastfm_user = lastfm.get_lastfm_user(sys.argv[1], sys.argv[2])
    except lastfm.WrongCredentialsException:
        print('Wrong LastFM credentials.')  # GUI => dialog window
        input()
        return

    loved_tracks = lastfm.get_loved_tracks_list(lastfm_user)
    spotify_username = sys.argv[3]
    playlist_name = sys.argv[4]

    return loved_tracks, spotify_username, playlist_name


if __name__ == '__main__':
    lastfm_fav_to_spotify_playlist()
