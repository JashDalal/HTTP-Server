#!/usr/bin/python3
import socket

localhost = '127.0.0.1'
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

#Bind address to the socket. Address is a combination of ip + port no.
s.bind(('', port))

s.listen(10) #Queue upto 10 request to the server.

while True:
	clientSocket, address = s.accept() #Accept TCP client connection; waits until connection arrives.
	#print("Got connection from server " + str(address))
	
	#open file contents into 'myfile' variable
	with open('post.html', 'r') as myfile:
	  data = myfile.read()
	
	#add headers to data
	a = "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: " + str(len(data)) + "\n\n" + str(data)
	
	clientSocket.sendall(bytes(a, "ascii"))
	myfile.close()
	s.close()
