# shows a user's playlists (need to be authenticated via oauth)

from __future__ import print_function
import os
import webbrowser
from spotipy import oauth2
import spotipy

from callback_server import callback_server


def prompt_for_user_token(username, scope=None, client_id=None,
                          client_secret=None, redirect_uri=None):
    ''' prompts the user to login if necessary and returns
        the user token suitable for use with the spotipy.Spotify 
        constructor

        Parameters:

         - username - the Spotify username
         - scope - the desired scope of the request
         - client_id - the client id of your app
         - client_secret - the client secret of your app
         - redirect_uri - the redirect URI of your app

    '''

    if not client_id:
        client_id = os.getenv('SPOTIPY_CLIENT_ID')

    if not client_secret:
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

    if not redirect_uri:
        redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

    if not client_id:
        raise spotipy.SpotifyException(550, -1, 'no credentials set')

    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri,
                                   scope=scope)

    auth_url = sp_oauth.get_authorize_url()
    callbackServer = callback_server.CallbackServer()

    webbrowser.open(auth_url)

    callbackServer.wait_for_request()
    while callbackServer.url == '':
        pass
    response = callbackServer.url

    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)

    if token_info:
        return token_info['access_token']
    else:
        return None
