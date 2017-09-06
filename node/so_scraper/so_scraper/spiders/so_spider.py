import scrapy
from so_scraper.items import SoScraperItem
from scrapy.loader import ItemLoader

class so_spider(scrapy.Spider):
	name = "so_question"

	def start_requests(self):
		urls = [
			'https://stackoverflow.com/questions?page=2&sort=newest',
			'https://stackoverflow.com/questions?page=3&sort=newest',
		]
		for url in urls:
			scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		QUESTION_SELECTOR = '.question-summary'
		for question in response.css(QUESTION_SELECTOR):
			loader = ItemLoader(item=SoScraperItem(), response=question)
			TAG_SELECTOR = '.post-tag ::text'
			VIEW_SELECTOR = '.views ::text'
			VOTE_SELECTOR = '.vote-count-post ::text'
			ANSWER_SELECTOR = '.status answered ::text'
			yield{
				loader.add_css('tags', TAG_SELECTOR)
				loader.add_css('views', VEIW_SELECTOR)
				loader.add_css('votes', VOTE_SELECTOR)
				loader.add_css('answers', ANSWER_SELECTOR)
				loader.load_item()
			}
		
