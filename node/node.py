import socket
import sys
import os
import signal
import re
import array
import scraper #Scraper Klasse die es mit dem Arbeitspaket vorzubereiten gilt
from requests import get
from scrapy.crawler import CrawlerProcess
from so_scraper.so_scraper.spiders import so_spider

distributor_ip = "139.6.65.29" #IP des Verteilers
distributor_port = 45678          #Port des Verteilprozesses
path = '/distributor'

#Verbindung zum Verteiler aufbauen
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((distributor_ip, distributor_port))

#Schleife 
while True:
    #Empfang des Start Sgnals
    sig = s.recv()
	print ("Start Signal erhalten:" + sig)
    #Pruefung des Signals
    #if not isinstance(sig, int):
    #    continue
    #Holen eines Arbeitspakets und Vorbereiten des CrawlProzesses in Schleife bis der Verteiler
    #False als Packet sendet
    package = get(distributor_ip + path)
	print ("Arbeitspaket erhalten" + package[1][0])
    while package not False:
        process = CrawlerProcess({'USER_AGENT': package[0], 'LOG_ENABLED': False})
        process.crawl(so_spider.so_spider, start_urls = package[1])
        process.start()
		print("crawl abgeschlossen")
        package = get(distributor_ip + path)
