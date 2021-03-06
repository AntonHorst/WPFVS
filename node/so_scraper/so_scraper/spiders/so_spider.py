import scrapy
from .. import items 
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join

class so_spider(scrapy.Spider):
	print("###########Start Spider###########")
	name = "so_spider"
	#start_urls = ['https://stackoverflow.com/questions?page=2000&sort=newest', 'https://stackoverflow.com/questions?page=3000&sort=newest']
	custom_settings = {
		'ITEM_PIPELINES': {'so_scraper.so_scraper.pipelines.ResultPipeline': 300},
		'DOWNLOADER_MIDDLEWARES': {'scrapy.downloadermiddlewares.retry.RetryMiddleware': None, 'so_scraper.so_scraper.middlewares.SleepRetryMiddleware': 100,},
		'DOWNLOAD_DELAY': 0.1,
	}
	def start_requests(self):
		print("###########Start Requests############")
		#urls = [
		#	'https://stackoverflow.com/questions?page=2000&sort=newest',
		#	'https://stackoverflow.com/questions?page=3000&sort=newest',
		#]
		with open("/Users/webcrawler/Projects/WPFVS/node/so_scraper/so_scraper/spiders/urls.txt", "rt") as f:
			self.start_urls = [url.strip() for url in f.readlines()]
		print(self.start_urls)
		for link in self.start_urls:
			print("########Verarbeite: " + link + "########")
			yield scrapy.Request(url=link, callback=self.parse)

	def parse(self, response):
		print("##########entered Parse##########")
		QUESTION_SELECTOR = '.question-summary'
		for question in response.css(QUESTION_SELECTOR):
			l = ItemLoader(item=items.SoScraperItem(), selector=question)
			TAG_SELECTOR = '.post-tag ::text'
			VIEW_SELECTOR = '.views ::text'
			VOTE_SELECTOR = '.vote-count-post ::text'
			ANSWER_SELECTOR = '//strong/text()'
			#UNANSWERED_SELECTOR = '.status unanswered ::text'
			#answers = question.css('.status')
			l.add_css('tags', TAG_SELECTOR)
			#l.add_value('tagAmount', len(question.css(TAG_SELECTOR)))
			l.add_css('views', VIEW_SELECTOR)
			l.add_css('votes', VOTE_SELECTOR)
			l.add_xpath('answers', ANSWER_SELECTOR)
			#l.add_css('answers', UNANSWERED_SELECTOR)
			yield l.load_item()
			"""	
			yield{
				'views': question.css(VIEW_SELECTOR).extract(),
				'votes': question.css(VOTE_SELECTOR).extract(),
				'answer': question.css(ANSWER_SELECTOR).extract(),
				'tags': question.css(TAG_SELECTOR).extract()
			}
			"""

			
		
