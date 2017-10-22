from .. import MobBro as DroidBro
from .. import BeautifulSoup as bs
from dateutil.parser import parse
from datetime import datetime
from urllib.parse import urljoin
from pprint import pprint

class Mobl(DroidBro):
	TRUSTED = ['koumkouat', 'Balatan']
	def search_query(self, query):
		base = 'http://forum.mobilism.org/searchapp.php?keywords={}&terms=all&sc=1&sf=titleonly&sk=t&sd=d&sr=topics&t=0&fid%5B%5D=400&fid%5B%5D=409'
		return self.get(base.format(query)).soup
	
	def txt(self, dom, **kwargs):
		return self.soup.find(dom, kwargs).string

	def entry_parse(self, soup):
		self.soup = soup
		user = self.txt('author')
		if user in self.TRUSTED:
			user = '[%s]'%user

		class Entry:
			time = self.parse_time('posttime')
			author = user
			title = self.txt('title')
			link = soup.find('link').next.strip()
			views = self.txt('views')
			topicid = self.txt('topicid')
		return Entry()

	def parse_time(self, dom):
		time = self.txt(dom)
		time = parse(time, fuzzy=True)
		time = datetime.now()-time

		return time

	def static_vars(self, i):
		return [getattr(i,x) for x in dir(i) if not x.startswith("__")]

	def sp(self, s):
		pprint(self.static_vars(s))

	def search(self, query):
		result_raw = self.search_query(query)
		try:
			entries = result_raw.topics.find_all('entry')
		except AttributeError:
			print(result_raw)
			return
		result = []

		for entry in entries:
			entry = self.entry_parse(entry)
			# self.sp(entry)
			result.append(entry)

		result.sort(key=lambda x:x.time)

		return result

	def fetch_topic(self, topicid):
		page = self.get(urljoin('http://forum.mobilism.org', topicid))

		page = page.text.encode('utf-8-sig').decode('utf-8')
		
		page = self._soup(page)
		page = page.find('content')

		txt = lambda el:page.find(el).string

		user = txt('author')
		if user in self.TRUSTED:
			user = '[%s]'%user
		class Content:
			app = txt('app')
			author = user
			img = txt('img')
			require = txt('require')
			overview = txt('overview')
			info = txt('info')
			dls = [i.link.next.strip() for i in page.downloads]

		return Content() 
