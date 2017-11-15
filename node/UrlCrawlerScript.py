from scrapy.crawler import Crawler
from scrapy.conf import settings
from scrapy import log 
from twisted.internet import reactor
from billiard import Process
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from threading import Thread
from scrapy.crawler import signals

#Diese Klasse bereitet einen Twisted Reactor vor, der mittels Process geforked wird und somit mehrfach ausgefuehrt werden kann
class UrlCrawlerScript(Process):
	def __init__(self, spider, userAgent):
		Process.__init__(self)
		#settings = {'USER_AGENT': userAgent, 'LOG_ENABLED': False}
		#settings['USER_AGENT': userAgent]
		BSettings = Settings()
		BSettings.set('USER_AGENT', userAgent, 30)
		BSettings.set('LOG_ENABLED', False, 30)
		self.crawler = Crawler(spider, BSettings)
		#self.crawler.configure()
		self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
		#self.userAgent = userAgent
		self.spider = spider

	def run(self):
		self.crawler.crawl(self.spider)
		#self.crawler.start()
		reactor.run()
		#process = CrawlerProcess({'USER_AGENT': self.userAgent, 'LOG_ENABLED': False})
		#process.crawl(self.spider)
		#Thread(target=process.start).start()
