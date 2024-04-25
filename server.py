import os
import http.server
import socketserver

from http import HTTPStatus
from mastodon import Mastodon

# Create an instance of the Mastodon class
mastodon = Mastodon(
    access_token='8HfPqIU2__o9sOhjVLEojEVPyI4LvLR4GXlJeNJZ9rU',
    api_base_url='https://dgpath.space'
)

def handle_mention(status):
    if '@system' in status.content:
        mastodon.status_post('@' + status.account.username + ' 테스트 출력입니다')

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        msg = 'Hello! you requested %s' % (self.path)
        mastodon.stream_user(handle_mention)
        self.wfile.write(msg.encode())



port = int(os.getenv('PORT', 80))
print('Listening on port %s' % (port))
httpd = socketserver.TCPServer(('', port), Handler)
httpd.serve_forever()
