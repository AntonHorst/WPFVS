import sys
import getopt
from collections import deque, defaultdict
from flask import Flask, request, abort
from flask_restful import reqparse, Api, Resource
import socket
from requests import get
from serv import Server
import threading
import time
import json
#Vorbereitung der Rest Api
app = Flask(__name__)
api = Api(app)

class Distributor(Resource):
	limit = 999412
	with open("/Users/webcrawler/Projects/WPFVS/distributor/useragent.txt", "rt") as f:
		agent = [userAgent.strip() for userAgent in f.readlines()]
	i=0
	ua_counter=0

	results = defaultdict(str) #{'tag':[views,answers,votes]}


	#gibt das nachste Arbeitspaket in der Form [UserAgent, [urls]] zurueck und False, falls kein Paket mehr vorhanden ist
	def getNextPackage(self):
		if self.i <= self.limit:
			current_agent = self.agent[self.ua_counter]
			package =[]
			urls =[]
			print (self.i)	
			if self.i+50 < self.limit:
				rangelimit = 50
			else:
				rangelimit = self.limit - self.i

			for j in range(self.i, self.i + rangelimit):
				urls.append('https://stackoverflow.com/questions?page=' + str(j) + '&sort=newest')
				j = j +1
				
			package.append(current_agent)
			package.append(urls)
		
			if type(self).ua_counter >= len(self.agent)-1:  
				type(self).ua_counter=0
			else:
				type(self).ua_counter+=1
				
			type(self).i += rangelimit
			print ("Paket vorhanden, wird returned")
			return package
		else:	#wird nicht erreicht, da i niemals groesser als das limit wird
			print("Kein Paket vorhanden")
			return False
	

	#Ueberträgt ein Arbetispaket an ein anfragenden Node
	def get(self):
		package = self.getNextPackage()
		if len(package[1]) == 0:
			print("QUE: INHALT DES ARBEITSPAKETS LEER: SENDE 404")
			print(type(self).results)
			abort(404)
		return {'package': package}
	
	#Empfaengt fuer jeden Tag die Views, Votes und Answers
	#Aufruf ueber put(apiPath, data={'tag': tag, 'votes': votes, 'answers': answers, 'views': views})
	def put(self):
		print('REST: put request erhalten')
		tag = request.form['tag']
		votes = int(request.form['votes'])
		answers = int(request.form['answers'])
		views = int(request.form['views'])
		print (tag + " " + str(votes) + " " + str(answers) + " " + str(views))
		if tag in type(self).results:
			type(self).results[tag][0] = type(self).results[tag][0] + votes
			type(self).results[tag][1] = type(self).results[tag][1] + answers 
			type(self).results[tag][2] = type(self).results[tag][2] + views
		else:
			type(self).results[tag] = [votes, answers, views]
		print ("Ergebniss gespeichert")
		#print(type(self).results)
		return 201


	
def main(argv):
	node_ip = ''
	node_port = 5000
	node_apiPath = 'node'
	apiPath = 'test'
	helpstring ="python distrib_que.py -n Node IP -p node Port -a Api_Path_Node"
	try:
		opts, args = getopt.getopt(argv, 'hn:p:a:', ['node=', 'port=', 'apipath=', 'help'])
	except getopt.Getopt.Error:
		print(helpstring)
		sys.exit(2)
	for opt, arg in opts:
		if opt in  ['-h', '--help']:
			print(helpstring)
			sys.exit(2)
		if opt in ['-n', '--node']:
			node_ip = str(arg)
		if opt in ['-p','--port']:
			node_port = arg
		if opt in ['-a','--api']:
			node_apiPath = arg
	apiPath = 'http://' + node_ip + ':' + str(node_port) + '/' + node_apiPath
	print (apiPath)
	
#def startRoutine():
	print("StartRoutine...")

	#Socket ueber einen Thread im Hintergrund starten(bleibt bis zum Schluss geoeffnet)
	print("Socket starten")
	server = Server()
	socketThread = threading.Thread(target=server.startServ)
	socketThread.setDaemon(True)
	socketThread.start()

	#Verbindung mit NodeREST aufbauen und Pagecount erhalten
	print("Versuche pagecount zu erhalten")
	#apiPath = 'http://localhost:5000/node'
	retry = True
	while retry:
		try:
			print(apiPath)
			r = get(apiPath)
		except:
			print("Node Rest nicht erreicht")
			time.sleep(10)
			continue
		retry = False

	#Pagecount aus der Antwort extrahieren
	json_accebtable_string = r.text.replace("'","/")
	rDict = json.loads(json_accebtable_string)
	pageCount = rDict['data']
	
	#print (r)
	#pageCount = int(r.text) 
	print ("Pagecount erhalten: " + pageCount)
	#set limit
	limit = 999412
	api.add_resource(Distributor, '/distributor')
if __name__ == '__main__':
	main(sys.argv[1:])
	#startRoutine()
	print("Start Routine abgeschlossen")
	app.run(host="0.0.0.0", port =45678, debug = True, use_reloader = False)


