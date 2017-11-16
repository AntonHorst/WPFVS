# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

"""
Evtl müssen die in und output Processoren noch für alle Felder definiert werden
"""

import re
import scrapy
from scrapy.loader.processors import MapCompose

"""
str ist wie folgt aufgebaut: "12 views"
die Methode gibt den vorne stehenden Integer Wert zurück
"""
def parseInt(string1):
	return int(re.search(r'\d+',string1).group())

#def parseList(liste):
#	l = ''.join(map(str, liste))
#	return l


class SoScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	tags = scrapy.Field()
	votes = scrapy.Field()
	answers = scrapy.Field(
		input_processor=MapCompose(parseInt),
	)
	#Aufruf der parseViews Methode beim fuellen des Fields über einen Loader
	views = scrapy.Field(
		input_processor=MapCompose(parseInt),
#		#output_processor=TakeFirst(),
	)



