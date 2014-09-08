
import sys
from twisted.python import log
log.startLogging(sys.stdout)

from twisted.internet import reactor, task
from datetime import datetime
from autobahn.websocket import (
    WebSocketClientFactory,
    WebSocketClientProtocol,
    connectWS
)
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

LOGIN_NAME = ''
LOGIN_PASS = ''

def get_key_val(resp, key):
    soup = BeautifulSoup(resp.text)
    return soup.find(attrs={'name' : key})['value']
     
session = requests.Session()
r = session.get('http://stackoverflow.com/users/login')
fkey = get_key_val(r, 'fkey')
payload = {
    'openid_identifier': 'https://openid.stackexchange.com',
    'openid_username': '',
    'oauth_version': '',
    'oauth_server': '',
    'fkey': fkey,
}
r = session.post('http://stackoverflow.com/users/authenticate', data=payload)
fkey = get_key_val(r, 'fkey')
session_name = get_key_val(r, 'session')

payload = {
    'email': LOGIN_NAME,
    'password': LOGIN_PASS,
    'fkey': fkey,
    'session': session_name
}
r = session.post('https://openid.stackexchange.com/account/login/submit', data=payload)
log.msg('Joining room')
r = session.get('http://chat.stackoverflow.com/rooms/6/python')
log.msg('Getting chat fkey for ws auth')
fkey = get_key_val(r, 'fkey')
auth_resp = session.post('http://chat.stackoverflow.com/ws-auth', data={'roomid': 6, 'fkey':fkey}).text
log.msg(auth_resp)
ws_url = json.loads(auth_resp)['url']
log.msg('URL: {}'.format(ws_url))
# r = session.post('http://chat.stackoverflow.com/chats/6/messages/new', data={'text': 'testing 123', 'fkey': fkey})

def send(text=None):
	#print dir(factory)
	if text is None:
		text = 'Time now: {} and {} messages seen'.format(datetime.now(), factory.message_counter)
	#print 'sending', text
	session.post('http://chat.stackoverflow.com/chats/6/messages/new', data={'text': text, 'fkey': fkey})



class ChatFeedProtocol(WebSocketClientProtocol): 
    def onOpen(self):        
        log.msg('Connected to chat feed')
        self.factory.message_counter = 0
        send()
        update.start(300, False)
    def onMessage(self, msg, binary):
        #log.msg(msg)    
        self.factory.message_counter += 1

if __name__ == '__main__':	
	log.msg('Attempting to connect to {}'.format(ws_url))
	factory = WebSocketClientFactory(
		ws_url + '?l=0', 
		useragent='sopython', 
		origin='http://chat.stackoverflow.com',
		debug=False
	)
	factory.protocol = ChatFeedProtocol
	connectWS(factory)
	#reactor.callLater(5, send, 'Started: {!s} - cabbage to all'.format(datetime.now()))
	update = task.LoopingCall(send)
	


	reactor.run()