import socket
import sys
import os
import signal
import re
import array
from requests import get
from scrapy.crawler import CrawlerProcess
from so_scraper.so_scraper.spiders import so_spider
import json

distributor_ip = "139.6.65.29" #IP des Verteilers
distributor_port = 31337          #Port des Verteilprozesses
apiPath = 'http://139.6.65.29:45678/distributor'

#Verbindung zum Verteiler aufbauen
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
retry = True
while retry:
	try:
		s.connect((distributor_ip, distributor_port))
	except socket.error:
		print ("Verbindungsaufbau Fehlgeschlagen")
		time.sleep(10)
		continue
ping = s.recv(1024)
if ping == 'OK':
	print("OK erhalten")
else:
	print("Abbruch: Fehlerhaftes Signal erhalten")
	sys.exit()
s.close()
print("Verbindung geschlossen")

#Schleife 
while True:
	#Holen eines Arbeitspakets und Vorbereiten des CrawlProzesses in Schleife bis der Verteiler
	#Keinen 200er HTTP Status mehr sendet
	try:
		resp = get(apiPath)
	except:
		print("Distributor REST API noch nicht bereit, schlafen fuer 10 Sekunden")
		time.sleep(10)
		continue
	if resp.is_success():
		print ("Arbeitspaket erhalten")
		json_acceptable_string = resp.text.replace("'","/")
		respDict = json.loads(json_acceptable_string)
		userAgent = respDict['package'][0]
		urls = respDict['package'][1]
		process = CrawlerProcess({'USER_AGENT': userAgent, 'LOG_ENABLED': False})
		process.crawl(so_spider.so_spider, start_urls = urls)
		process.start()
		print("crawl abgeschlossen")
	else:
		print("Kein weiteres Arbeitspaket vorhanden")
		#sys.exit() Etwas rabiat falls ein sonstiger Fehler auftaucht
