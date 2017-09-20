from flask_restful import reqparse, Api, Resource
from scrapy.Crawler import CrawlerProcess
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
		process = CrawlerProcess({'LOG_ENABLED': False}.append(stdUA))
		process.crawl(PageCountSpider)
		process.start()
		filename = 'count.txt'
		
		with open(filename, 'r'):
			count = f.read()
		return count

api.add_resource(Node, '/node')

if __name__ == '__main__':
	app.run(debug = True, use_reloader = False)
