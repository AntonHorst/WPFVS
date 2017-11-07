from flask import Flask
from flask_restful import reqparse, Api, Resource
from scrapy.crawler import CrawlerProcess
from so_scraper.so_scraper.spiders import PageCountSpider

app = Flask(__name__)
api = Api(app)

stdUA = {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'}
"""
@Author Till Hein
@Date 20.09.2017
Diese Klasse stellt eine (teilweise) Rest API zur verfuegung,ueber die 
der Verteiler die Gesamtanzahl der Seiten abrufen kann 
"""
class Node(Resource):
	def get(self):
		process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT %.1)','LOG_ENABLED': False})
		process.crawl(PageCountSpider.PageCountSpider)
		process.start()
		filename = 'count.txt'
		
		with open(filename, 'r') as f:
			count = f.read()

		print ("Anfordern des Pagecounts:" + count)

		return {'data': count}

api.add_resource(Node, '/node')

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug = True, use_reloader = False)
