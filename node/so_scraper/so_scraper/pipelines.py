from request import post
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
	apiPath = "http://139.6.65.29:5000/distributor"
    def process_item(self, item, spider):
        for tag in item['tags']:
            numbers = []
            numbers.append(item['votes'])
            numbers.append(item['answers'])
            numbers.append(item['views'])
            result = {tag: numbers}
            put(apiPath, data = result)
