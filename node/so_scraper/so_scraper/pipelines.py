from requests import put
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SoScraperPipeline(object):
	def process_item(self, item, spider):
		answers=item['answers'][1]
		filename = 'output.txt'
		with open(filename, 'a') as f:
			f.write(answers)
		return item

class ResultPipeline(object):
	#print("##########Entered Pipeline#########")
	apiPath = "http://139.6.65.29:45678/distributor"
	def process_item(self, item, spider):
		for tag in item['tags']:
			if item['answers'] = None:
				item['answers'] = 0
			put(self.apiPath, data={'tag': tag, 'votes': item['votes'], 'answers': item['answers'], 'views': item['views']})
