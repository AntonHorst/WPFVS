import scrapy
from .. import items 
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join

class so_spider(scrapy.Spider):
	name = "so_spider"

	def start_requests(self):
		#urls = [
		#	'https://stackoverflow.com/questions?page=2000&sort=newest',
		#	'https://stackoverflow.com/questions?page=3000&sort=newest',
		#]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		QUESTION_SELECTOR = '.question-summary'
		for question in response.css(QUESTION_SELECTOR):
			l = ItemLoader(item=items.SoScraperItem(), selector=question)
			TAG_SELECTOR = '.post-tag ::text'
			VIEW_SELECTOR = '.views ::text'
			VOTE_SELECTOR = '.vote-count-post ::text'
			IF '.status answered ::true':
				ANSWER_SELECTOR = '.status answered  ::text'
			ELSE:
				ANSWER_SELECTOR = '0'
			#UNANSWERED_SELECTOR = '.status unanswered ::text'
			answers = question.css('.status')
			l.add_css('tags', TAG_SELECTOR)
			#l.add_value('tagAmount', len(question.css(TAG_SELECTOR)))
			l.add_css('views', VIEW_SELECTOR)
			l.add_css('votes', VOTE_SELECTOR)
			l.add_css('answers', ANSWER_SELECTOR)
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

			
		
