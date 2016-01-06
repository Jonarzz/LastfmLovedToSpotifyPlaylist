"""Test module for the spotify module."""

import unittest

import spotify
import properties

__author__ = 'Jonarzz'


class SpotifyTest(unittest.TestCase):
    """Class used to test spotify module.
    Inherits from TestCase class of unittest module."""
    token = None
    spotify_obj = None
    loved_tracks = [{'artist': 'wrong_artist_name', 'title': 'wrong_title'},
                    {'artist': 'metallica', 'title': 'master of puppets (live)'},
                    {'artist': 'Parov Stelar', 'title': 'The Sun feat. Graham Candy'}]
    expected_search_queries = ['wrong_artist_name wrong_title',
                               'metallica master of puppets',
                               'Parov Stelar The Sun']
    playlist_id = None

    def test_1_generate_token(self):
        """Method testing Spotify API token generation. Needs to be run as first, because
        generated token is used in further tests."""
        SpotifyTest.token = spotify.generate_token()
        self.assertIsNotNone(SpotifyTest.token)

    def test_2_create_spotify_object(self):
        """Method testing spotipy.Spotify object creation. Needs to be run as second, because
        generated object is used in further tests."""
        SpotifyTest.spotify_obj = spotify.create_spotify_object(self.token)
        self.assertIsNotNone(SpotifyTest.spotify_obj)

    def test_calculate_progress(self):
        """Method used to test calculate_progress method from the spotify module."""
        self.assertEqual(spotify.calculate_progress(1, 2), '50.00%')
        self.assertEqual(spotify.calculate_progress(1, 3), '33.33%')
        self.assertEqual(spotify.calculate_progress(1, 100), '1.00%')
        self.assertEqual(spotify.calculate_progress(1, 200), '0.50%')
        self.assertEqual(spotify.calculate_progress(1, 2000), '0.05%')

    def test_create_search_query(self):
        """Method used to test creating search queries - the created queries are compared
        to expected ones (sorted lists are compared)."""
        search_queries = []
        for track in SpotifyTest.loved_tracks:
            search_queries.append(spotify.create_search_query(track))

        self.assertTrue(sorted(search_queries) == sorted(SpotifyTest.expected_search_queries))

    def test_get_track_id_from_search_query(self):
        """Method used to test getting Spotify tracks IDs based on a given search query."""
        expected_tracks_ids = [None, '6NwbeybX6TDtXlpXvnUOZC', '5ahvjrjn7ymaeaWKFZrsca']
        tracks_ids = []
        for query, track in list(zip(SpotifyTest.expected_search_queries,
                                     SpotifyTest.loved_tracks)):
            tracks_ids.append(spotify.get_track_id_from_search_query(SpotifyTest.spotify_obj,
                                                                     query,
                                                                     track['artist']))

        self.assertEqual(tracks_ids, expected_tracks_ids)

    def test_create_spotify_tracks_ids_list_from_loved(self):
        """Method used to test creation of a list of tracks IDs based on given loved tracks
        dictionaries with usage of spotipy.Spotify object. Created list is compared with
        expected list (both sorted)."""
        expected_tracks_ids = ['6NwbeybX6TDtXlpXvnUOZC', '5ahvjrjn7ymaeaWKFZrsca']
        tracks_ids = spotify.create_spotify_tracks_ids_list_from_loved(SpotifyTest.loved_tracks,
                                                                       SpotifyTest.spotify_obj)

        self.assertTrue(sorted(tracks_ids) == sorted(expected_tracks_ids))

    def test_3_create_playlist_for_user(self):
        """Method testing if a playlist creation using Spotify API was successful."""
        SpotifyTest.playlist_id = spotify.create_playlist_for_user(SpotifyTest.spotify_obj,
                                                                   properties.SPOTIFY_TEST_USERNAME,
                                                                   'test')
        self.assertIsNotNone(SpotifyTest.playlist_id)

    def test_add_tracks_to_playlist(self):
        """Method testing if adding tracks to a playlist using Spotify API was successful."""
        results = spotify.add_tracks_to_playlist(SpotifyTest.spotify_obj,
                                                 properties.SPOTIFY_TEST_USERNAME,
                                                 SpotifyTest.playlist_id,
                                                 ['6NwbeybX6TDtXlpXvnUOZC',
                                                  '5ahvjrjn7ymaeaWKFZrsca'])

        self.assertNotEqual(results, [])
