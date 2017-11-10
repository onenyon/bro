from . import SessionX
from logging import getLogger
from requests.exceptions import ConnectionError
from time import sleep
log = getLogger(__name__)

class Rip:
	BRO = SessionX()
	def __init__(self, url):
		self._url   = url
		self._limit = None
		self._soup  = None
		self._next  = None
		self._func  = None

	def no_soup(self):
		return not self._soup

	def cook(self, cookies):
		self.BRO.cookies = cookies
		return self

	def next(self, selector):
		self._next = selector
		return self

	def func(self, _func):
		self._func = _func
		return self

	def limit(self, n):
		self._limit = n
		return self

	def _run(self):
		try:
			resp = self.BRO.get(self._url)
		except ConnectionError:
			print('URL:', self._url)
			print('Server ConnectionError.\nEither no Internet Connection or Server Down.')
		else:
			if not resp.ok:
				log.info('{} Retrying after 5 seconds.'.format(resp.text))
				resp.close()
				sleep(5)
				return self._run()
			self._soup = resp.soup
			self._func(self)

	def _select(self, selector, one=False):
		elements =  set(self._soup.select(selector))
		if selector is True:
			length = len(elements)
			if length == 1:
				return elements.pop()
			print('Element is more than one because Length is', length)
		return elements

	# def find(self, ):
	# 	if self.no_soup():
	# 		print('Soup is empty')
	# 	return

	def _next_url(self):
		if callable(self._next):
			_next_url = self._next(self)
		else:
			_next_url = self._select(self._next, True).get('href', None)
		return _next_url

	def _set_next(self):
		next_url = self._next_url()
		if not next_url:
			return False
		self._url = next_url
		log.debug('Next url: %s'%self._url)
		return True

	def _has_limit(self):
		limit = self._limit is not None
		if limit:
			self._limit -= 1
			print(self._limit , 'Pages Left')
			limit = self._limit == 0
		return not limit

	def run(self):
		self._run()
		if self._next:
			if not self._set_next():
				print('The Last url is', self._url)
				return

			if not self._has_limit():return

			# if self._limit is not None:
			# 	self._limit-=1
			# 	print(self._limit , 'Pages Left')
			# if self._limit == 0:
			# 	return
			self.run()