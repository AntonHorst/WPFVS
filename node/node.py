import socket
import sys
import os
import signal
import re
import array
from requests import get
from scrapy.crawler import CrawlerRunner
from so_scraper.so_scraper.spiders import so_spider
from twisted.internet import reactor
import json
import time
from UrlCrawlerScript import UrlCrawlerScript
import getopt


distributor_ip = "127.0.0.1" #IP des Verteilers
distributor_port = 31337          #Port des Verteilprozesses
apiPath = 'http://localhost:45678/distributor'

def main(argv):
	distributor_ip = ''
	distributor_port = 0
	api_port = 0
	api_path = 'distributor'
	helpstring = "node.py -d Distributor_IP -p Distributor_Port -a APIPort (-A APIPath)"
	try:
		opts, args = getopt.getopt(argv, "hd:p:a:A:", ["help", "distributorip=", "distributorport=", "apiport=", "apipath"]
	except:
		print(helpstring)
		sys.exit(2)
	for opt,arg in opts:
		if opt in ('-h', '--help'):
			print(helpstring)
			sys.exit(2)
		elif opt in ('-d', '--distributorip'):
			distributor_ip = arg
		elif opt in ('-p', '--distributorport'):
			distributor_port = arg
		elif opt in ('-A', '--apiPath'):
			api_path = arg
		elif opt in ('-a', '--apiport'):
			api_port = arg
			apiPath = 'http://'+ distributor_ip + ':' + distributor_port + '/' + api_path
		
	#Verbindung zum Verteiler aufbauen
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	retry = True
	while retry == True:
		try:
			retry = False
			s.connect((distributor_ip, distributor_port))
		except socket.error:
			retry = True
			print ("Verbindungsaufbau Fehlgeschlagen")
			time.sleep(10)
			continue
	
	ping = s.recv(1024)
	print (str(ping))
	if str(ping) == "b'OK'":
		print("OK erhalten")
	else:
		print("Abbruch: Fehlerhaftes Signal erhalten")
		sys.exit()
	s.close()
	print("Verbindung geschlossen")
	
	while True:
		#Vorbereiten des CrawlerObjekts
		spider = so_spider.so_spider()
		crawler = UrlCrawlerScript(spider)
	
		#Holen eines Arbeitspakets und Vorbereiten des CrawlProzesses in Schleife bis der Verteiler
		#Keinen 200er HTTP Status mehr sendet
		try:
			resp = get(apiPath)
		except:
			print("Distributor REST API noch nicht bereit, schlafen fuer 10 Sekunden")
			time.sleep(10)
			continue
		if resp.status_code == 200:
			print ("Arbeitspaket erhalten")
			json_acceptable_string = resp.text.replace("'","/")
			respDict = json.loads(json_acceptable_string)
			userAgent = respDict['package'][0]
			urls = respDict['package'][1]
			print("Rufe Spider mit UA:" + userAgent + "auf")
			#Start des crawl Prozesses
			crawler.runSoSpider(userAgent, urls)
			print("crawl abgeschlossen")
		else:
			print("Kein weiteres Arbeitspaket vorhanden")
			sys.exit() #Etwas rabiat falls ein sonstiger Fehler auftaucht

if name == "__main__":
	main(sys.argv[1:])
