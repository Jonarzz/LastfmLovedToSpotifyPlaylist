"""Test module for the lastfm module."""

import unittest

import pylast

import lastfm
import properties

__author__ = 'Jonarzz'


class LastfmTest(unittest.TestCase):
    """Class used to test lastfm module.
    Inherits from TestCase class of unittest module."""

    def test_get_lastfm_user(self):
        """Method testing the connection to the LastFM API and to the given account."""
        self.assertRaises(lastfm.WrongCredentialsException,
                          lastfm.get_lastfm_user,
                          properties.LASTFM_TEST_USERNAME, 'wrong_password')

        user = lastfm.get_lastfm_user(properties.LASTFM_TEST_USERNAME,
                                      properties.LASTFM_TEST_PASSWORD)
        self.assertIsNotNone(user)

        name = user.get_name()
        playcount = user.get_playcount()

        self.assertEqual(name, properties.LASTFM_TEST_USERNAME)
        self.assertEqual(playcount, 0)

    def test_get_loved_tracks(self):
        """Method testing get_loved_tracks method of lastfm module - tests if the returned value
        is not None."""
        user = lastfm.get_lastfm_user(properties.LASTFM_TEST_USERNAME,
                                      properties.LASTFM_TEST_PASSWORD)
        loved_tracks = lastfm.get_loved_tracks(user)

        self.assertIsNotNone(loved_tracks)

    def test_create_track_dict(self):
        """Method testing create_track_dict method of lastfm module - tests if for the mocked
        LovedTrack object a correct dictionary is returned."""
        for i in range(3):
            track_artist = 'test{}_artist'.format(i)
            track_title = 'test{}_track'.format(i)
            expected_dict = {'artist': track_artist, 'title': track_title}

            track = pylast.Track(track_artist, track_title, None)
            loved_track = pylast.LovedTrack(track, None, None)

            output_dict = lastfm.create_track_dict(loved_track)

            self.assertEqual(output_dict, expected_dict)

    def test_get_loved_tracks_list(self):
        """Method testing get_loved_tracks method which retrives loved tracks for a given user
        and creates a list of dictionaries."""
        user = lastfm.get_lastfm_user(properties.LASTFM_TEST_USERNAME,
                                      properties.LASTFM_TEST_PASSWORD)
        loved_tracks_list = lastfm.get_loved_tracks_list(user)

        expected_output = [{'artist': 'Freddy The Flying Dutchman & The Sistina Band',
                           'title': 'Wojtyla Disco Dance'},
                           {'artist': 'Desire', 'title': 'Under Your Spell'}]

        for output in expected_output:
            self.assertTrue(output in loved_tracks_list)
