import scrapy

class PageCountSpider(scrapy.Spider):
	name="PageCountSpider"

	def start_requests(self):
		urls = [
			'https://stackoverflow.com/questions'
		]

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		page_fl_selector= ".pager"
		page_number_selector = ".page-numbers ::text"
		numberpart = response.css(page_fl_selector)
			
			#'count': numberpart.css(page_number_selector).extract()[6],
		filename='count.txt'
		with open(filename, 'w') as f:
			f.write(numberpart.css(page_number_selector).extract()[6])
	
