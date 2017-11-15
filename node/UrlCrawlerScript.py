from scrapy.crawler import Crawler
from scrapy.conf import settings
from scrapy import log, project
from twisted.internet import reactor
from billiard import Process
from scrapy.utils.project import get_project_settings

#Diese Klasse bereitet einen Twisted Reactor vor, der mittels Process geforked wird und somit mehrfach ausgefuehrt werden kann
class UrlCrawlerScript(Process):
	def __init__(self, spider, userAgent):
		Process.__init__(self)
		settings = get_project_settings()
		settings['USER_AGENT': userAgent]
		self.crawler = Crawler(settings)
		self.crawler.configure()
		self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
		self.spider = spider

	def run(self):
		self.crawler.crawl(self.spider)
		self.crawler.start()
		reactor.run()
