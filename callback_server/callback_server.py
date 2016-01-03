"""Module used to start a server waiting to be called by the callback url
defined for the Spotify API. Attempts to close the card with url opened
in the browser with a script. Query parameters from the url called are used
later to obtain Spotify API token."""

import http.server

import properties

__author__ = 'Jonarzz'


class CallbackServer:
    """Class used to create a server and respond for one request on specified port."""
    url = ''

    class _MyHandler(http.server.BaseHTTPRequestHandler):
        """Inner class subclassing BaseHTTPRequestHandler to define the response to
         GET request."""
        def do_GET(self):
            """Method specifying the response to a GET request.

            HTTP code is set to 200. HTML body sent is taken from the properties file.
            Script in the payload HTML code attempts to close the card in which the callback
            url was opened. If it fails, an information about closing the card is written out.
            """
            CallbackServer.url = self.path
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(properties.CALLBACK_RESPONSE_BODY)

    @staticmethod
    def wait_for_request(server_class=http.server.HTTPServer,
                         handler_class=_MyHandler):
        """Method used to start a server on specified port and accept one request."""
        server_address = ('', properties.PORT)
        httpd = server_class(server_address, handler_class)
        httpd.handle_request()
