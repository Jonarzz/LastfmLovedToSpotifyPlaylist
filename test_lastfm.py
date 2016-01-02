"""Test module for the lastfm module."""

import unittest

import pylast

import lastfm

__author__ = 'Jonarzz'


class LastfmTest(unittest.TestCase):
    """Class used to test lastfm module.
    Inherits from TestCase class of unittest module."""

    def test_get_lastfm_user(self):
        """Method testing the connection to the LastFM API and to the given account."""
        user = lastfm.get_lastfm_user('dummy_test_acc', 'test1!')

        self.assertEqual(user.get_name(), 'dummy_test_acc')
        self.assertEqual(user.get_playcount(), 0)

    def test_get_loved_tracks(self):
        """Method testing get_loved_tracks method of lastfm module - tests if the returned value
        is not None."""
        self.assertIsNotNone(lastfm.get_loved_tracks('dummy_test_acc', 'test1!'))

    def test_create_track_dict(self):
        """Method testing create_track_dict method of lastfm module - tests if for the mocked
        LovedTrack object a correct dictionary is returned."""
        for i in range(3):
            track_artist = 'test{}_artist'.format(i)
            track_title = 'test{}_track'.format(i)
            expected_dict = {'artist': track_artist, 'title': track_title}
            track = pylast.Track(track_artist, track_title, None)
            loved_track = pylast.LovedTrack(track, None, None)
            self.assertEqual(lastfm.create_track_dict(loved_track), expected_dict)

    def test_get_loved_tracks_list(self):
        """Method testing get_loved_tracks method which retrives loved tracks for a given user
        and creates a list of dictionaries."""
        self.assertEqual(lastfm.get_loved_tracks('dummy_test_acc', 'test1!'),
                         [{'artist': 'Freddy The Flying Dutchman & The Sistina Band',
                           'title': 'Wojtyla Disco Dance'}])
