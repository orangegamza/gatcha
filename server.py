import os
import http.server
import socketserver

from http import HTTPStatus
from mastodon import Mastodon
from mastodon.streaming import StreamListener

# Create an instance of the Mastodon class
mastodon = Mastodon(
    access_token='8HfPqIU2__o9sOhjVLEojEVPyI4LvLR4GXlJeNJZ9rU',
    api_base_url='https://dgpath.space'
)

listener = dgListener()
mastodon.stream_user(listener)
answers = "TEST"

class dgListener(StreamListener):
    def on_notification(self, notification):
        if notification[’type’] == ’mention’:
            id = notification[’status’][’id’]
            visibility = notification[’status’][’visibility’]
            mastodon.status_post(answers, in_reply_to_id = id, visibility = visibility)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        msg = 'Hello! you requested %s' % (self.path)
        mastodon.stream_user(listener)
        self.wfile.write(msg.encode())

port = int(os.getenv('PORT', 80))
print('Listening on port %s' % (port))
httpd = socketserver.TCPServer(('', port), Handler)
httpd.serve_forever()
