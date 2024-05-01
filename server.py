import os
import http.server
import socketserver

from http import HTTPStatus
from mastodon import Mastodon
from mastodon.streaming import StreamListener

from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Create an instance of the Mastodon class
mastodon = Mastodon(
    access_token='8HfPqIU2__o9sOhjVLEojEVPyI4LvLR4GXlJeNJZ9rU',
    api_base_url='https://dgpath.space'
)



# 구글 스프레드시트 세팅
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         ]

# 비공개 키 (Credential key) 파일 이름 (.json)
# 해당 파일은 본 파일과 같은 폴더 안에 있어야 함.

credentials = ServiceAccountCredentials.from_json_keyfile_name("path-gatcha-85cf742b0be2.json", scope)

# 구글 스프레드시트에 연결
gc = gspread.authorize(credentials)

# 스프레드시트 열기 (스프레드시트 URL)
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1WufEcVPt0LyY7Awvflf9JU7ZlI91IKsp97gHwZc0LKA")

emblem = sh.worksheet("모두의 칭호")
gatcha = sh.worksheet("가챠")

def playGatcha(n):
    result = "기계가 돌아간다. 도르륵. 도르륵.\n"
    for i in range(n):
        gatcha.update_cell(4, 15, False)
        gatcha.update_cell(4, 15, True)
        result += "\n" + str(gatcha.cell(4, 14).value)
    return result

def upadateEmblem():
    emblem.update_cell(1, 1, False)
    emblem.update_cell(1, 1, True)




class dgListener(StreamListener):
    anwers = ''
    def on_notification(self, notification):
        if notification['type'] == 'mention':
            id = notification['status']['id']
            visibility = notification['status']['visibility']
            answers = "무언가 잘못된 것 같다..."
            if '[가챠]' in notification['status']['content']:
                if '1' in notification['status']['content']:
                    answers = playGatcha(1)
                elif '2' in notification['status']['content']:
                    answers = playGatcha(2)
                elif '3' in notification['status']['content']:
                    answers = playGatcha(3)
                elif '4' in notification['status']['content']:
                    answers = playGatcha(4)
                elif '5' in notification['status']['content']:
                     answers = playGatcha(5)
        
        mastodon.status_post("@" + notification['account']['username'] + "\n" + 
                            answers, in_reply_to_id = id, 
                            visibility = visibility)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        # msg = 'Hello! you requested %s' % (self.path)
        mastodon.stream_user(dgListener())
        # self.wfile.write(msg.encode())

port = int(os.getenv('PORT', 80))
print('Listening on port %s' % (port))
httpd = socketserver.TCPServer(('', port), Handler)

mastodon.stream_user(dgListener())

httpd.serve_forever()
