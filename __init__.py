from requests import Session
from bs4 import (BeautifulSoup, FeatureNotFound)
from urllib.parse import urlsplit

from time import sleep

class SessionX(Session):
	PARSER = 'html.parser'
	def _soup(self, content, **kwargs):
		return BeautifulSoup(content, self.PARSER, **kwargs)
		
	def soup(self, content, **kwargs):
		return self._soup(content, **kwargs)

	def send(self, request, **kwargs):
		r = super().send(request, **kwargs)
		r.soup = self.soup(r.text)
		return r

class Bro(SessionX):
	USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36'
	def __init__(self, url=None, *args, **kwargs):
		SessionX.__init__(self, *args, **kwargs)
		self.headers['user-agent'] = self.USER_AGENT
		if url:
			self.headers['host'] = urlsplit(url).netloc

	def request(self, url, method, **kwargs):
		req = super().request(url, method, **kwargs)
		if not req.ok:
			print('Request was not successful retrying after 5 seconds!')
			sleep(5)
			return self.request(url, method, **kwargs)
		return req

class MobBro(Bro):
	USER_AGENT = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7'

class DroidBro(Bro):
	USER_AGENT = 'User-Agent: Dalvik/2.1.0 (Linux; U; Android 7.0; SM-J710F Build/NRD90M)' # My sam pn

class Bot(Bro):
	USER_AGENT = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'