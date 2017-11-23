from scrapy.crawler import Crawler
#from scrapy.conf import settings
#from scrapy import log 
from twisted.internet import reactor
from billiard import Process
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from threading import Thread
from scrapy.crawler import signals
import os

#Diese Klasse bereitet einen Twisted Reactor vor, der mittels Process geforked wird und somit mehrfach ausgefuehrt werden kann
class UrlCrawlerScriptold(Process):
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

class UrlCrawlerScript():
	def __init__(self, spider):
		print("CrawlerObjekt erstellen")
		self.BSettings = Settings()
		self.BSettings.set('LOG_ENABLED', False, 30)
		#BSettings.set('USER_AGENT', userAgent, 30)
		#self.crawler = Crawler(spider, self.BSettings)
		#self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
		self.spider = spider

	def run(self, userAgent):
		print("Child Process erstellen")
		newPid = os.fork()
		if newPid == 0:
			print("entered Child")
			self.BSettings.set('USER_AGENT', userAgent, 30)
			crawler = Crawler(self.spider, self.BSettings)
			crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
			crawler.crawl(self.spider)
			reactor.run()
			os._exit(0)
		else:
			os.wait()

	def runSoSpider(self, userAgent, urls):
		print ("Child Prozess erstellen")
		newPid = os.fork()
		if newPid == 0:
			print("Child Prozess erstellt")
			self.BSettings.set('USER_AGENT', userAgent, 30)
			self.spider.start_urls = urls
			crawler = Crawler(self.spider, self.BSettings)
			crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
			crawler.crawl(self.spider)
			print("Fehlersuche")
			reactor.run()
			print("reactor.run ausgefuehrt")
			os._exit(0)
		else:
			os.wait()


