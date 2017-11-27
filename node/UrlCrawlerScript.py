from scrapy.crawler import Crawler
#from scrapy.conf import settings
#from scrapy import log 
from twisted.internet import reactor

from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from threading import Thread
from scrapy.crawler import signals
import os

class UrlCrawlerScript():
	def __init__(self, spider):
		print("CrawlerObjekt erstellen")
		self.BSettings = Settings()
		self.BSettings.set('LOG_ENABLED', False, 30)
		self.BSettings.set('COOKIES_ENABLED', False, 30)
		#BSettings.set('USER_AGENT', userAgent, 30)
		#self.crawler = Crawler(spider, self.BSettings)
		#self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
		self.spider = spider

	def run(self, userAgent):
		print("Spider wird aufgerufen")
		newPid = os.fork()
		if newPid == 0:
			print("Spider Prozess erfolgreich dupliziert")
			self.BSettings.set('USER_AGENT', userAgent, 30)
			crawler = Crawler(self.spider, self.BSettings)
			crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
			crawler.crawl(self.spider)
			reactor.run()
			os._exit(0)
		else:
			os.wait()

	def runSoSpider(self, userAgent, urls):
		print ("Spider wird aufgerufen")
		newPid = os.fork()
		if newPid == 0:
			print("Spider Prozess erfolgreich dupliziert")
			self.BSettings.set('USER_AGENT', userAgent, 30)
			#self.BSettings.set('ITEM_PIPELINES', {'so_scraper.pipelines.ResultPipeline': 300}, 30)
			#self.spider.start_urls = urls
			#URLS in Datei schreiben, um sie in der Spider einzulesen
			f = open('/Users/webcrawler/Projects/WPFVS/node/so_scraper/so_scraper/spiders/urls.txt', 'w')
			for url in urls:
				print (url)
				f.write("%s\n" %url)
			f.close()
			crawler = Crawler(self.spider, self.BSettings)
			crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
			crawler.crawl(self.spider)
			reactor.run()
			os._exit(0)
		else:
			os.wait()


