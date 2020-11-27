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



Each website runs on an Apache Web Server
When you access a URL, it is the Web Server of that website that you are sending requests to.

Try telneting to my machine over the same network and using port used in the code.

My HTTP Server handles client request till a client says quit
Error handling and header handling is done with status codes 403, 404, 405.

GET and POST request parameters are stored in a a CSV file called parameters.csv, created at runtime.
urllib.parse is used to decode the encoded url passed by the client
In the PUT request, a copy of the file the client wants to send is created on the server side.
