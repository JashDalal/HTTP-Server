"""Code to except multiple requests"""
from time import  gmtime, strftime
import time
from socket import *
from threading import Thread
import sys
import os
import os.path, time
import magic
import shutil
import pathlib
import csv
import filecmp

filread = open("server.conf","r")
r = (filread.read())
data1 = r.split ("\n")
dicti ={}
for c in range(len(data1) - 1):
	var = data1[c].split(" ")
	dicti.update({var[0]:var[1]})
for item in dicti:
	if 'MaxKeepAliveRequests' in item:
		MaxKeepAliveRequests = dicti['MaxKeepAliveRequests']
	if 'admin_flag' in item:
		admin_flag = dicti['admin_flag']
	if 'ServerRoot' in item:
		ServerRoot = dicti['ServerRoot']
	if 'ErrorLog' in item:
		ErrorLog = dicti['ErrorLog']

serverPort = 13000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
MaxKeepAliveRequests = int(MaxKeepAliveRequests)
serverSocket.listen(MaxKeepAliveRequests)
serverStatus = 'keep-alive'

#Function establish connection
def chat(connectionSocket, addr):
	print("New connection to client {}\n".format(addr))
	while True:
		text = connectionSocket.recv(1024).decode()
		print('Text from client {}: {}'.format(addr[1], text))
		
		#For splitting request
		newlinesplit = text.split('\r\n')
		firstlinesplit = []
		check = []
		var = []
		firstlinesplit = newlinesplit[0].split()
		if firstlinesplit[0] == 'exit()' or firstlinesplit[0] == 'quit()':
			serverStatus = 'Closed'
			message  = 'BYE'
			connectionSocket.send(message.encode())
			break
		
		#Splitting for last line
		if(len(newlinesplit) >= 3 and (firstlinesplit[0] != 'PUT' or firstlinesplit[0] != 'POST')):
			for i in range(1, len(newlinesplit) - 1):
				check.append(newlinesplit[i].split(":"))
		elif(len(newlinesplit) < 3):
			status =  ' 400 Bad Request'
			filename = '400.html'
			version = 'HTTP/1.1'
			date =  time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
			#Function to write in log file
			ErrorLogWrite(addr, status, date)
			headers(filename, connectionSocket,status, version)
		
		if(len(newlinesplit) >= 3):
			
			if len(firstlinesplit) != 3:
				status =  ' 400 Bad Request'
				filename = '400.html'
				version = 'HTTP/1.1'
				date =  time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
				ErrorLogWrite(addr, status, date)
				headers(filename, connectionSocket,status, version)
			else:
				if(firstlinesplit[0]):
					method =  firstlinesplit[0]
				
				if(firstlinesplit[1]):
					filename = firstlinesplit[1]
					if(filename[0] != '/'):
						status =  ' 400 Bad Request'
						filename = '400.html'
						version = 'HTTP/1.1'
						date =  time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
						#Function to write in log file
						ErrorLogWrite(addr, status, date)
						headers(filename, connectionSocket,status, version)
					else:
						if (filename[-1] == '/' and len(filename) == 1):
							filename = '/index.html'
						if(len(filename) != 1 and filename[-1] == '/'):
							filename = filename[:-1] + '/index.html'
						filename = ServerRoot + filename
				
				if(firstlinesplit[2]):
					version = firstlinesplit[2]
					if (version != 'HTTP/1.1' or (version == 'HTTP/1.1' and check[0][0] != 'Host')) :
						status =  ' 400 Bad Request'
						filename = '400.html'
						version = 'HTTP/1.1'
						date =  time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
						#Function to write in log file
						ErrorLogWrite(addr, status, date)
						headers(filename, connectionSocket,status, version)
				
				if(method == 'GET'):
					flag = 0
					i = 0
					if(filename.find("?") != -1):
						flag = 1
						do_urlget(filename, connectionSocket, version, addr)
					while(i < len(check)):
						if(check[i][0] == 'If-Modified-Since'):
							flag = 1
							do_conditional(filename, connectionSocket, check[i][1], version, addr)
							break
						i += 1
					if(flag == 0):
						do_get(filename, connectionSocket,version, addr)

				if(method == 'HEAD'):
					do_head(filename, connectionSocket, version, addr)

				if(method == 'PUT'):
					if(admin_flag != '1'):
						filename = '405.html'
						status = ' 405 Method Not Allowed'
						version = 'HTTP/1.1'
						headers(filename, connectionSocket,status, version)
					else:
						j = 0
						while(newlinesplit[j] != ''):
							j += 1
						j += 1
						data = ''
						while(j < len(newlinesplit)):
							data += newlinesplit[j]
							j += 1 
						do_put(connectionSocket, filename, version, data, addr)

				if(method == 'POST'):
					j = 0
					while(newlinesplit[j] != ''):
						j += 1
					j += 1
					data = ''
					while(j < len(newlinesplit)):
						data += newlinesplit[j]
						j += 1 
					do_post(connectionSocket, filename, version, data, addr)

				if(method == 'OPTIONS'):
					do_options(connectionSocket, filename, version)

				if(method == 'DELETE'):
					if(admin_flag != '1'):
						filename = '405.html'
						status = ' 405 Method Not Allowed'
						version = 'HTTP/1.1'
						date =  time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
						#Function to write in log file
						ErrorLogWrite(addr, status, date)
						headers(filename, connectionSocket,status, version)
					else:
						do_delete(connectionSocket, filename, version, addr)

				if((method != 'GET' and method.upper() == 'GET') or (method != 'HEAD' and method.upper() == 'HEAD') or (method != 'PUT' and method.upper() == 'PUT' ) or (method != 'OPTIONS' and method.upper() == 'OPTIONS') or (method != 'DELETE' and method.upper() == 'DELETE')):
					handle_501(filename, connectionSocket, version)
	
	connectionSocket.close()



#Function Handle headers
def headers(filename, connectionSocket,status, version):

	#To open file
	f = open(filename, "rb")
	
	file_content = f.read()
	filesize = file_size(filename)
	
	#To get file size
	content_length = "Content-Length: " + str(filesize)
	server_name = 'Server: Myserver'
	
	#To check wheather connection is closed or not
	
	Connection = 'Connection: ' + serverStatus
	
	date = '\nDate: ' + time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime()) 
	#To get last modified date
	mdate = time.ctime(os.path.getmtime(filename))
	modified_date = "Last modified date: " + mdate 
	
	

	#For Response Message
	response = '\n' + version + status + date + '\n' +  server_name  + '\n' + content_length + '\n' + modified_date + '\n' + Connection  + '\n'  + '\n'
	print("You: " , response)
	print(str(file_content))
	connectionSocket.send(response.encode())
	connectionSocket.sendfile(f)



#To handle 'GET' request
def do_get(filename, connectionSocket,version, addr):
	try:
		#to get filepath and to read file contents
		f = open(filename[1:])
		filename = filename[1:]
		status = ' 200 OK'
		
		headers(filename, connectionSocket,status, version)
		print("Done with file sending..\n")
	except IOError:
		filename = '404.html'
		status = ' 404 Not Found' 
		date =  time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
		#Function to write in log file
		ErrorLogWrite(addr, status, date)
		headers(filename, connectionSocket,status, version)
		

def do_urlget(filename, connectionSocket, version, addr):
	try:
		var = filename.split("?")
		var1 = []
		filename = var[0]
		for c in range(1, len(var)):
			variables = var[c].split("&")
			for k in range(len(variables)):
				var1.append(variables[k].split("="))
		with open('getdata.csv', 'w') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerows(var1)
		csvFile.close()
		f = open(filename[1:])
		filename = filename[1:]
		status = ' 200 OK'
		
		headers(filename, connectionSocket,status, version)
		print("Done with file sending..\n")
		
	except IOError:
		filename = '404.html'
		status = ' 404 Not Found' 

		date =  time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
		#Function to write in log file
		ErrorLogWrite(addr, status, date)
		headers(filename, connectionSocket,status, version)
		
			
#Function to handle HEAD request
def do_head(filename, connectionSocket, version, addr):
	try:
		#to get filepath and to read file contents
		f = open(filename[1:])
		filename = filename[1:]
		status = ' 200 OK'
		
		f = open(filename)
		filesize = file_size(filename)
		
		#To get file size
		content_length = "Content-Length: " + str(filesize)
		server_name = 'Server: Myserver'
	
		Connection = 'Connection: ' + serverStatus
	
		#For MIME type
		m = magic.open(magic.MAGIC_MIME)
		m.load()
		Type = 'Content-Type: ' + m.file(filename)
	
		#To get last modified date
		mdate = time.ctime(os.path.getmtime(filename))
		modified_date = "Last modified date: " + mdate 
		date = '\nDate: ' + time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())	

		#For Response Message
		response = '\n' + version + status  + date + '\n' +  server_name  + '\n' + content_length + '\n' + Type + '\n' + modified_date + '\n' + Connection + '\n'  + '\n'
		print("You: ", response)
		print("Done with file sending..\n")
		connectionSocket.send(response.encode())
	except IOError:
		filename = '400.html'
		status = ' 400 Bad Request' 
		f = open(filename)
		file_content = f.read()
		filesize = file_size(filename)
	
		#To get file size
		content_length = "Content-Length: " + str(filesize)
		server_name = 'Myserver'
		date = time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
		Connection = 'Connection: ' + serverStatus

		#For MIME type
		m = magic.open(magic.MAGIC_MIME)
		m.load()
		Type = 'Content-Type: ' + m.file(filename)
		
		date = '\nDate: ' + time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
		#Function to write in log file
		ErrorLogWrite(addr, status, date)

		#For Response Message
		response = '\n' + version + status +  date + '\n' + server_name + '\n' + content_length + '\n' + Connection + '\n'  + '\n'

		print("You: ", response)
		connectionSocket.send(response.encode())



#Function to calculate filesize	
def file_size(fname):
	statinfo = os.path.getsize(fname)
	return statinfo

#Function to 'Do Conditional Get'
def do_conditional(filename, connectionSocket, var, version, addr):
	try:
		f = open(filename[1:])
		filename = filename[1:]
		
		f = open(filename, "rb")
		file_content = f.read()
		filesize = file_size(filename)
	
		#To get file size
		content_length = "Content-Length: " + str(filesize)
		server_name = 'Server: Myserver'
	
		
		Connection = 'Connection: ' + serverStatus
	
		mdate = time.ctime(os.path.getmtime(filename))
		modified_date = "Last modified date: " + mdate 	

		#For MIME type
		m = magic.open(magic.MAGIC_MIME)
		m.load()
		Type = 'Content-Type: ' + m.file(filename)
		date = '\nDate: ' + time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime()) 
		sdate1 =  mdate.split()
		split1 = mdate.split()
		month1 = month_converter(split1[1])
		date1 =  split1[2]
		year1 = split1[4]
		split2 = var.split()
		flag = 0
		
		if (len(split2) < 5):
			flag = 1
			status = ' 200 OK'
			response = '\n' + version + status  + date + '\n' +  server_name  + '\n' + content_length + '\n' + Type + '\n' + Connection + '\n' + modified_date + '\n'  + '\n'
		
		if flag == 0:
			date2 =  split2[1]
			month2 = month_converter(split2[2])
			year2 = split2[3]
			if(int(year2) <= int(year1)):
				if(int(month1) > int(month2)):
					if(int(date1) > int(date2)):
						status = ' 304 Not Modified'
						response = '\n' + version + status + date + '\n' + server_name  + '\n' + content_length + '\n' + Connection + '\n'  + '\n'
				else:
					status = ' 200 OK'
					response = '\n' + version + status  + date + '\n' + server_name  + '\n' + content_length + '\n' + Connection + '\n'  + '\n'
					
			else:
				status = ' 304 Not Modified'
				response = '\n' + version + status  + date + '\n' + server_name  + '\n' + content_length + '\n' + Connection + '\n'  + '\n'
		print("You: ", response)
		print(str(file_content))
		print("\nDone with file sending..\n")
		connectionSocket.send(response.encode())
		
		connectionSocket.sendfile(f)
	except IOError:
		filename = '404.html'
		status = ' 404 Not Found' 
		f = open(filename)
		file_content = f.read()
		filesize = file_size(filename)
	
		#To get file size
		content_length = "Content-Length: " + str(filesize)
		server_name = 'Server: Myserver'
		Connection = 'Connection: ' + serverStatus
	
		#To get last modified date
		mdate = time.ctime(os.path.getmtime(filename))
		modified_date = "Last modified date: " + mdate 	

		#For MIME type
		m = magic.open(magic.MAGIC_MIME)
		m.load()
		Type = 'Content-Type: ' + m.file(filename)
		
		date =  time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
		#Function to write in log file
		ErrorLogWrite(addr, status, date)
	
		date = '\nDate: ' + time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
		#For Response Message
		response = '\n' + version + status + date + '\n' + server_name  + '\n' + content_length + '\n' + Connection + '\n'  + '\n'
		print("You: ", response)
		connectionSocket.send(response.encode())




#Function to handle 'PUT' request
def do_put(connectionSocket, filename, version, data, addr):
	f = open('temp', "w+")
	for c in data:
		f.write(c)
	print(f.read())
	filename = filename[1:]
	#filesize = file_size(filename)
	if (os.path.exists(filename) != True):
		os.rename("temp", filename)
		status = ' 201 Created'
	else:
		if(filecmp.cmp(filename, "temp")):
			status = ' 204 Not Modified'
		else:
			os.remove(filename)
			os.rename('temp', filename)
			status = ' 200 OK'

	server_name = 'Server: Myserver'
	Connection = 'Connection: ' + serverStatus
	
	#For MIME type
	m = magic.open(magic.MAGIC_MIME)
	m.load()
	Type = 'Content-Type: ' + m.file(filename)
	date = '\nDate: ' + time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
	#To get file size
	#content_length = "Content-Length: " + str(filesize)
	
	#For Response Message
	response = '\n' + version + status + date + '\n'  + server_name  + '\n' + Type + '\n' + Connection + '\n'  + '\n'
	print("You: ", response)
	print("\n Done with file uploading...")
	connectionSocket.send(response.encode())
	
		

def do_post(connectionSocket, filename, version, data, addr):
	try:
		var1 = []
		var = data.split('&')
		for c in range(len(var)):
			var1.append(var[c].split("="))
		
		with open('postdata.csv', 'w') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerows(var1)
		csvFile.close()
		
		
		f = open(filename[1:], "rb")
		filename = filename[1:]
		status = ' 200 OK'
		
		headers(filename, connectionSocket,status, version)
		print("File is created successfully...\n")
	except IOError:
		filename = '404.html'
		status = ' 404 Not Found' 
		#For writing in log file
		date =  time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
		#Function to write in log file
		ErrorLogWrite(addr, status, date)
		headers(filename, connectionSocket,status, version)
		
#For handling 501 request
def handle_501(filename, connectionSocket, version, addr):
	filename = '501.html'
	status = ' 501 Not Implemented'
	
	date =  time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())

	#Function to write in log file
	ErrorLogWrite(addr, status, date)
	headers(filename, connectionSocket, status, version)


#For 'OPTIONS' request
def do_options(connectionSocket, filename, version):
	
	status =  ' 200 OK'
	content_length = "Content-Length: 0"
	server_name = 'Server: Myserver'
	Connection = 'Connection: ' + serverStatus
	m = magic.open(magic.MAGIC_MIME)
	m.load()
	date = '\nDate: ' + time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
	if admin_flag == '1':
		allow_requests = 'Allow: GET, POST, HEAD, OPTIONS, PUT , DELETE'
	else:
		allow_requests = 'Allow: GET, POST, HEAD, OPTIONS'

	response = '\n' + version + status + date + '\n' + server_name  + '\n' + allow_requests + '\n' + content_length + '\n' + '\n' + Connection + '\n'  + '\n'
	print("You: ", response)
	connectionSocket.send(response.encode())
	
		


#Function to handle 'DELETE' request
def do_delete(connectionSocket, filename, version, addr):
	try:
		#f = open(filename[1:], "rb")
		filename = filename[1:]
		status = ' 200 OK'
		f = open('deleted.html')
		file_content = f.read()
		filesize = file_size(filename)
	
		#To get file size
		content_length = "Content-Length: " + str(filesize)
		server_name = 'Server: Myserver'
	
		#To check wheather connection is closed or not
	
		Connection = 'Connection: ' + serverStatus
	
		#For MIME type
		m = magic.open(magic.MAGIC_MIME)
		m.load()
		Type = 'Content-Type: ' + m.file(filename)
	
		date = '\nDate: ' + time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
		#For Response Message
		response  = '\n' + version + status  + date + '\n' +  server_name  + '\n' + Type + '\n' + content_length + '\n' + Connection + '\n' + file_content +  '\n' + '\n'
		os.remove(filename)
		print("You: ", response)
		print("\nFile is deleted  successfully")
		connectionSocket.send(response.encode())
	except IOError:
		filename = '404.html'
		status = ' 404 Not Found' 
		f = open(filename)
		file_content = f.read()
		filesize = file_size(filename)
	
		#To get file size
		content_length = "Content-Length: " + str(filesize)
		server_name = 'Server: Myserver'
	
		#To check wheather connection is closed or not
		
		Connection = 'Connection: ' + serverStatus
		
		#For MIME type
		m = magic.open(magic.MAGIC_MIME)
		m.load()
		Type = 'Content-Type: ' + m.file(filename)
		
		date =  '\nDate: ' + time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
		
		#For Response Message
		response = '\n'+ version + status  + date + '\n' + server_name  + '\n' + content_length + '\n' + Connection + '\n' + Type + '\n' + file_content + '\n' 
		
		#Function to write in log file
		ErrorLogWrite(addr, status, date)
		
		print("You: ", response)
		connectionSocket.send(response.encode())

def month_converter(month):
	months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	return months.index(month) + 1

def ErrorLogWrite(addr, status, date):
	f2 = open(ErrorLog, "a")
	port_no = str(addr[0])
	client_addr  = str(addr[1])
	towrite = port_no + ',' + client_addr + '\n' + date + '\n' + status + '\n'
	f2.write(towrite)
		
def main():
	print('The server is ready to receive...')
	while True:
		connectionSocket, addr = serverSocket.accept()
		t = Thread(target=chat, args=(connectionSocket, addr))
		t.start()
	for t in threads:
		t.join()
	serverSocket.close()





main()


