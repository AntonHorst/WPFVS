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
