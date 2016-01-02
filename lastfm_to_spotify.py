"""Main module of the LastfmLovedToSpotifyPlaylist project."""

import sys

import lastfm
import spotify

__author__ = 'Jonasz'


def main():
    """Main method of the module and project that brings together other modules using APIs."""
    loved_tracks = lastfm.get_loved_tracks_list('dummy_test_acc', 'test1!')
    spotify_username = 'orzeu89'
    playlist_name = 'test3'
    try:
        token = spotify.generate_token(spotify_username)
    except spotify.TokenGenerationException:
        print('Error generating token.')
    else:
        sp = spotify.create_spotify_object(token)
        tracks_ids = spotify.create_spotify_tracks_ids_list_from_loved(loved_tracks, sp)
        playlist_id = spotify.create_playlist_for_user(sp, spotify_username, playlist_name)
        spotify.add_tracks_to_playlist(sp, spotify_username, playlist_id, tracks_ids)


if __name__ == '__main__':
    main()
