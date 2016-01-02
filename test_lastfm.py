"""Test module for the lastfm module."""

import unittest

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
        """Method testing get_loved_tracks method which retrives lvoed tracks for a given user."""
        self.assertEqual(lastfm.get_loved_tracks('dummy_test_acc', 'test1!'),
                         [{'artist': 'Freddy The Flying Dutchman & The Sistina Band',
                           'title': 'Wojtyla Disco Dance'}])
