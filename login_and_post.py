import requests
from bs4 import BeautifulSoup


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
r = session.get('http://chat.stackoverflow.com/rooms/6/python')
fkey = get_key_val(r, 'fkey')
r = session.post('http://chat.stackoverflow.com/chats/6/messages/new', data={'text': 'testing 123', 'fkey': fkey})
