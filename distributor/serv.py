import socket
import sys #zum beenden
import time #fuer delay beim versenden des "pings"
import threading

class Server:
	def __init__(self):
		print ("Server Objekt wird erstellt")	

	#Funktion die die eingehenden Connections handhabt und regelmaessig den Ping versendet
	def clientthread(self, conn):
		ping = "OK"
		while True:
			time.sleep(15)
			print ("Send Ping: " + ping)
			try:
				conn.sendall(ping.encode('utf-8'))
			except:
				print("Connection closed by client")
				break
			#reply = conn.recv(1024)
			#if not reply:
				#break
		conn.close()
	
	#Funtion die den Server startet
	def startServ(self):
		HOST = ''
		PORT = 31337 
		MAX_WAITING_CONNECTIONS = 20
		
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print ("Socket erstellt")
		
		try:
			s.bind((HOST, PORT))
		except:
			print ("Socket Bind fehlgeschlagen: ErrCode: " + str(msg[0]) + ", ErrMsg: " + msg[1])
			sys.exit()
		print ("Socket bind abgeschlossen")
		
		s.listen(MAX_WAITING_CONNECTIONS)
		print("Socket listening. Max Waiting Connections: " + str(MAX_WAITING_CONNECTIONS))
		
		#Auf Nodes warten und regelmaessig ping versenden 
		while True:
			conn, addr = s.accept()
			print ("Verbunden mit: " + addr[0] + ":" + str(addr[1]))
			clientThread = threading.Thread(target=self.clientthread, args=(conn,))
			clientThread.daemon = True
			clientThread.start()
			#start_new_thread(clientthread, (conn,))
		
		#Socket schliessen
		s.close
		print("Socket geschlossen")
