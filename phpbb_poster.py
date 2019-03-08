import time
import configparser
import requests
from bs4 import BeautifulSoup as BS
from requests_toolbelt import sessions

config = configparser.ConfigParser()
config.read('config.ini')

forum = config.sections()[0]
login = "/ucp.php?mode=login"
forum_number = config[forum]['forum_number'] # 17 == Pull Requests
post = "/posting.php?mode=post&f={}".format(forum_number)

headers = {'User-Agent': 'Mozilla/5.0'}
login_payload = {'redirect': 'index.php',
                 'sid': '',
                 'login': 'Login'}
login_payload['username'] = config[forum]['username']
login_payload['password'] = config[forum]['password']

def grab_secrets(soup):
    # DEBUG: print(soup)
    # DEBUG: print(dir(soup))
    form_token = soup.find('input', {'name': 'form_token'})['value']
    lastclick = soup.find('input', {'name': 'lastclick'})['value']
    creation_time = soup.find('input', {'name': 'creation_time'})['value']
    return form_token, lastclick, creation_time

def make_topic(new_topic_request):
    soup = BS(new_topic_request.text, "lxml")
    form_token, lastclick, creation_time = grab_secrets(soup)
    data = {'post': 'Submit', 
            'lastclick': creation_time,
            'creation_time': creation_time,
            'form_token': form_token}
    return data

def new_topic(subj, msg):
    with sessions.BaseUrlSession(base_url=forum) as s:
        login_request = s.post(forum + login, headers=headers, data=login_payload)
        # DEBUG: print(login_request.text)
        soup = BS(login_request.text, "lxml")
        time.sleep(2.5)
        # DEBUG: print(soup)
        new_topic_request = s.get(forum + post, headers=headers)
        data = make_topic(new_topic_request)
        data['subject'], data['message'] = subj, msg
        time.sleep(2.5) # phpbb gives a 302 error if form is submitted immediately
        new_topic = s.post(post, headers=headers, data=data)

if __name__ == '__main__':
    subj = 'test subject goes here'
    msg = 'test message goes here'
    new_topic(subj, msg)
