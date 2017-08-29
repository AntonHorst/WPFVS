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
		output = []
		for url in urls:
			output.append(scrapy.Request(url=url, callback=self.parse))
		return output

	def parse(self, response):
		output = []
		QUESTION_SELECTOR = 'question-summary'
		for question in response.css(QUESTION_SELECTOR):
			output_part = []
			loader = ItemLoader(item=SoScraperItem(), response=question)
			TAG_SELECTOR = 'post-tag'
			VIEW_SELECTOR = 'views'
			VOTE_SELECTOR = 'vote-count-post'
			ANSWER_SELECTOR = 'status answered'
			loader.add_css('tags', TAG_SELECTOR)
			loader.add_css('views', VEIW_SELECTOR)
			loader.add_css('votes', VOTE_SELECTOR)
			loader.add_css('answers', ANSWER_SELECTOR)
			loader.load_item()
			output_part.append(item['tags'])
			output_part.append(item['views'])
			output_part.append(item['votes'])
			output_part.append(item['answers'])
			output.append(output_part)
		return output
		
