# HTTP-Server
An implementation of a simple web server to handle HTTP requests and responses

An HTTP Server has to be made which can process 
1. GET
2. POST
3. PUT
4. HEAD
5. DELETE
6. PATCH
7. OPTIONS

Basic format of a GET/POST request is:
	<p>
	POST <relative path> HTTP/1.1
	Host: <hostname>
	name1=value1&name2=value2
	</p>
For eg:
	POST /test/demo_form.php HTTP/1.1
	Host: w3schools.com
	name1=value1&name2=value2
	
	
A sample GET request response is of this format.

Request:	
	GET /index.html HTTP/1.1
	Host: www.jashdalal.tk

Response:
	HTTP/1.1 200 OK
	Date: Sun, 08 Sep 2019 13:21:33 GMT
	Content-Type: text/html; charset=UTF-8
	Transfer-Encoding: chunked
	Connection: keep-alive
	Accept-Ranges: bytes
	Server: awex
	X-Xss-Protection: 1; mode=block
	X-Content-Type-Options: nosniff
	X-Request-ID: 014b08001ab3a45e646a292accff714b

	<html>
	<h1 align = "center"> Jash Dalal</h1>
	</html>

Each website runs on an Apache Web Server
When you access a URL, it is the Web Server of that website that you are sending requests to.

Try telneting to my machine over the same network and using port used in the code
GET The index.html page rendered by My HTTP Server

telnet localhost 80
GET /index.html HTTP/1.1
Host:localhost

HTTP/1.1 200 OK
Date: Fri, 13 Sep 2019 11:03:47 GMT
Server: Apache/2.4.29 (Ubuntu)
Last-Modified: Sun, 08 Sep 2019 13:03:40 GMT
ETag: "2aa6-5920a4cd8d95c"
Accept-Ranges: bytes
Content-Length: 10918
Vary: Accept-Encoding
Content-Type: text/html

<HTML PAGE index.html is rendered by Apache stored in index.html>

My HTTP Server handles client request till a client says quit
Error handling and header handling is done with status codes 403, 404, 405.

GET and POST request parameters are stored in a a CSV file called parameters.csv, created at runtime.
urllib.parse is used to decode the encoded url passed by the client


PUT request syntax:

PUT /new.html HTTP/1.1
Host: example.com
Content-type: text/html
Content-length: 16

PUT Response syntax:
HTTP/1.1 201 Created
Content-Location: /new.html

HTTP/1.1 200 OK
Content-Location: /new.html

In the PUT request, a copy of the file the client wants to send is created on the server side.
Then it is moved to the destined location
This requires chmod 755 <folder name> to hold otherwise we cannot read and write into the folder

501 Method Not Implemented
HTTP/1.1 501 Not Implemented
Date: Tue, 01 Oct 2019 11:08:29 GMT
Server: Apache/2.4.29 (Ubuntu)
Allow: POST,OPTIONS,HEAD,GET
Content-Length: 278
Connection: close
Content-Type: text/html; charset=iso-8859-1

304 Not Modified
HTTP/1.1 304 Not Modified
Date: Wed, 02 Oct 2019 10:26:52 GMT
Server: Apache/2.4.29 (Ubuntu)
ETag: "2aa6-5920a4cd8d95c"
