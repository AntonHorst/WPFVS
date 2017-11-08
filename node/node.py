import socket
import sys
import os
import signal
import re
import array
import requests
from scrapy.crawler import CrawlerProcess
from so_scraper.so_scraper.spiders import so_spider
import json

distributor_ip = "139.6.65.29" #IP des Verteilers
distributor_port = 45678          #Port des Verteilprozesses
path = '/distributor'
apiPath = 'http://139.6.65.29:5000/distributor'

#Verbindung zum Verteiler aufbauen
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((distributor_ip, distributor_port))

#Schleife 
while True:
    #Empfang des Start Sgnals
	sig = -1
    sig = s.recv()
	if sig == 1:
    	print ("Start Signal erhalten:" + sig)
    	#Holen eines Arbeitspakets und Vorbereiten des CrawlProzesses in Schleife bis der Verteiler
    	#Keinen 200er HTTP Status mehr sendet
    	resp = get(apiPath)
    	while resp.is_success():
    		print ("Arbeitspaket erhalten")
    		json_acceptable_string = resp.text.replace("'","/")
    		respDict = json.loads(json_acceptable_string)
    		userAgent = respDict['package'][0]
    		urls = respDict['package'][1]
    	    process = CrawlerProcess({'USER_AGENT': userAgent, 'LOG_ENABLED': False})
    	    process.crawl(so_spider.so_spider, start_urls = urls)
    	    process.start()
    	    print("crawl abgeschlossen")
    	    resp = get(apiPath)
