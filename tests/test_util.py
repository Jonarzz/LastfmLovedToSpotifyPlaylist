"""Module testing the changed util module from spotipy library."""

import unittest

import spotipy

import my_spotipy.util as util
import properties

__author__ = 'Jonarzz'


class UtilTest(unittest.TestCase):
    """Class used to test util module from spotipy library.
    Inherits from TestCase class of unittest module."""

    def test_prompt_for_user_token(self):
        self.assertRaises(spotipy.SpotifyException,
                          util.prompt_for_user_token)

        token = util.prompt_for_user_token(properties.MODIFY_PLAYLISTS_SCOPE,
                                                   properties.SPOTIFY_API_ID,
                                                   properties.SPOTIFY_API_SECRET,
                                                   properties.SPOTIFY_REDIRECT_URL)
        self.assertIsNotNone(token)
