'''This file is to test file handling. First we'll have to get the file path from the client, 
open the file to read it. Then we add whatever headers we like and send it to the client socket.'''
from time import strftime
import os.path, time
import csv
import shutil
import getpass
#import magic
with open('index.html', 'r') as myfile:
  data = myfile.read()
  a = "HTTP/1.1 200 OK\nContent-Type: text/plain\nContent-Length: 12\n\n" + str(data)
  print(a)
  myfile.close()
  
a = input("Please enter a string")

print(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
print(time.ctime(os.path.getmtime("file.py")))
print(os.path.getsize("file.py"))
#magic.from_file('file.py', mime=True)

import mimetypes 
filename = "index.html"
print(mimetypes.MimeTypes().guess_type(filename)[0])



path = 'Error/404.html'
data = ''
path1 = '/index.html'
if(path1.startswith('/')):
	path1 = path1[1:]
with open(path1, 'r') as myfile:
	data = myfile.read()
	print(data)


headers = dict([('A','1'), ('B', '2'), ('C', '3')])
abc = '\n'.join("{}:{}".format(key,val) for (key,val) in headers.items())
	
print(abc)

'''
path = "/Error/index.html"
index = path.rfind('/')
file_path = path[1:index]
shutil.copy2("jash.html", file_path)
'''
path = "/jash.html"
with open("copy", 'w') as f:
	with open("jash.html", "r") as source:
		data = source.read()
		f.write(data)
f.close()
source.close()


	
print("Username: Umash/1.0.0")
password = getpass.getpass(prompt='Password: ', stream=None)


file_path = "Error/"
shutil.move("copy", file_path)
	




