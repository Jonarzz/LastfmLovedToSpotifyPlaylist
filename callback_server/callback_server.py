import http.server

import properties

__author__ = 'Jonarzz'


class CallbackServer:
    url = ''

    def __init__(self):
        pass

    class _MyHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            CallbackServer.url = self.path
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(properties.CALLBACK_RESPONSE_BODY)

    @staticmethod
    def wait_for_request(server_class=http.server.HTTPServer,
                         handler_class=_MyHandler):
        server_address = ('0.0.0.0', properties.PORT)
        httpd = server_class(server_address, handler_class)
        httpd.handle_request()
