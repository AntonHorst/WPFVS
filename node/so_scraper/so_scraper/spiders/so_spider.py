import scrapy
from so_scraper.items import SoScraperItem
from scrapy.loader import ItemLoader

class so_spider(scrapy.Spider):
	name = "so_questions"

	def start_requests(self):
		urls = [
			'https://stackoverflow.com/questions?page=2&sort=newest',
			'https://stackoverflow.com/questions?page=3&sort=newest',
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		QUESTION_SELECTOR = '.question-summary'
		for question in response.css(QUESTION_SELECTOR):
			l = ItemLoader(item=SoScraperItem(), response=response)
			TAG_SELECTOR = '.post-tag ::text'
			VIEW_SELECTOR = '.views ::text'
			VOTE_SELECTOR = '.vote-count-post ::text'
			ANSWER_SELECTOR = '.status answered ::text'
			
			l.add_css('tags', TAG_SELECTOR)
			l.add_css('views', VIEW_SELECTOR)
			l.add_css('votes', VOTE_SELECTOR)
			l.add_css('answers', ANSWER_SELECTOR)
			return l.load_item()
			"""	
			yield{
				'views': question.css(VIEW_SELECTOR).extract(),
				'votes': question.css(VOTE_SELECTOR).extract(),
				'answer': question.css(ANSWER_SELECTOR).extract(),
				'tags': question.css(TAG_SELECTOR).extract()
			}
			"""

			
		
