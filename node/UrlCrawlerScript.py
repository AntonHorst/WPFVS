from scrapy.crawler import CrawlerProcess
from scrapy.conf import settings
from scrapy import log 
from twisted.internet import reactor
from billiard import Process
from scrapy.utils.project import get_project_settings
from scrapy.settings import BaseSettings

#Diese Klasse bereitet einen Twisted Reactor vor, der mittels Process geforked wird und somit mehrfach ausgefuehrt werden kann
class UrlCrawlerScript(Process):
	def __init__(self, spider, userAgent):
		Process.__init__(self)
		#settings = get_project_settings()
		#settings['USER_AGENT': userAgent]
		BSettings = BaseSettings()
		BSettings.set('USER_AGENT', userAgent, 30)
		BSettings.set('LOG_ENABLED', False, 30)
		self.crawler = CrawlerProcess(spider)
		self.crawler.configure()
		self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
		self.spider = spider

	def run(self):
		self.crawler.crawl(self.spider)
		self.crawler.start()
		reactor.run()
