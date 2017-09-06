# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

"""
Evtl müssen die in und output Processoren noch für alle Felder definiert werden
"""


import scrapy
from scrapy.loader.processors import Compose
"""
str ist wie folgt aufgebaut: "12 views"
die Methode gibt den vorne stehenden Integer Wert zurück
"""
def parseViews(str):
	return int(str.split(' ', 1)[0])

class SoScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	tags = scrapy.Field()
	votes = scrapy.Field()
	answers = scrapy.Field()
	#Aufruf der parseViews Methode beim füllen des Fields über einen Loader
	views = scrapy.Field(
		input_processor=Compose(parseViews),
		#output_processor=TakeFirst(),
	)



