"""File containing properties for the LastfmLovedToSpotifyPlaylist project."""

__author__ = 'Jonarzz'

PORT = 80

LASTFM_API_KEY = ''
LASTFM_API_SECRET = ''

SPOTIFY_API_ID = ''
SPOTIFY_API_SECRET = ''
SPOTIFY_REDIRECT_URL = '{}'.format(PORT)

MODIFY_PLAYLISTS_SCOPE = 'playlist-modify-public'

TITLE_ENDINGS_TO_CUT = [' ft. ', ' ft ', ' feat ', 'feat. ', '(']

CALLBACK_RESPONSE_BODY = b"<script>window.open('', '_self', '');" \
                         b"window.close();</script>" \
                         b"<p>Please, close the tab, if it was not closed.</p>"
