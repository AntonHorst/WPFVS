import socket
import sys

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print ("Verbindung zum Socket Fehlgeschlagen")
	sys.exit()

print ("Socket erstellt")

HOST = '139.6.65.29'
PORT = 31337

s.connect((HOST, PORT))
print ("Verbunden mit: " + HOST + ":" + str(PORT))

ping = s.recv(1024)
if ping == 'OK':
	print("OK erhalten")
s.close()
print("Verbindung geschlossen")
