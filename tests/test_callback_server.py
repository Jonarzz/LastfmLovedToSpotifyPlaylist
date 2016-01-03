"""Module used to test callback_server module."""

import unittest
import urllib.request
import threading

from callback_server import callback_server
import properties

__author__ = 'Jonarzz'


class CallbackServerTest(unittest.TestCase):
    """Class used to test callback_server module.
    Inherits from TestCase class of unittest module."""

    def test_init(self):
        """Method used to test initialization of CallbackServer object."""
        cb_server = callback_server.CallbackServer()
        self.assertIsNotNone(cb_server)
        self.assertEqual(cb_server.url, '')

    def test_wait_for_request(self):
        """Method used to test if the callback server is running and responding as expected."""
        server_thread = threading.Thread(target=callback_server.CallbackServer.wait_for_request)
        server_thread.start()

        request = urllib.request.urlopen(properties.SPOTIFY_REDIRECT_URL)
        http_code = request.getcode()
        response_body = request.read()

        self.assertEqual(http_code, 200)
        self.assertEqual(response_body, properties.CALLBACK_RESPONSE_BODY)
