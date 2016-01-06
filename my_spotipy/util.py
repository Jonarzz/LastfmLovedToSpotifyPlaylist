"""Shows a user's playlists (need to be authenticated via oauth)."""

from __future__ import print_function
import webbrowser
from spotipy import oauth2
import spotipy

from callback_server import callback_server


def prompt_for_user_token(scope=None, client_id=None,
                          client_secret=None, redirect_uri=None):
    """ Prompts the user to login if necessary and returns
        the user token suitable for use with the spotipy.Spotify 
        constructor

        Parameters:
         - scope - the desired scope of the request
         - client_id - the client id of your app
         - client_secret - the client secret of your app
         - redirect_uri - the redirect URI of your app
    """
    if not client_id:
        raise spotipy.SpotifyException(550, -1, 'No credentials set')

    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)

    auth_url = sp_oauth.get_authorize_url()
    cb_server = callback_server.CallbackServer()

    webbrowser.open(auth_url)

    cb_server.wait_for_request()

    response = cb_server.url

    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)

    return token_info['access_token']
