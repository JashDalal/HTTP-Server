

HTTP server handles the following requests :
1)GET 
	a)GET - It sends '200 OK' response when entered file name is correct and if file doesn't exist it sends 	'404NotFound'.File is sent through socket  
	b)Conditional GET - It sends '304 Not Modified' if file not updated, precision is upto date,'200 OK' response when      
	file name is correct and if file 	doesn't exist it sends '404 Not Found' 
	c)GET with parameters - We store URL parameters in CSV file which named as 'getdata.csv'
2)POST 
	Parameters come into the body through which the CSV file is made, if the file exists it sends '200 OK' as response and 	if the file doesn't not exist then it sends '404 Not Found'  	
3)HEAD
	Headers are passed and last modified is considered to be the main header,HEAD sends '400 Bad Request' when the given 		file doesn't exist  
4)PUT
	'201 created' is sent when the file doesn't exist and new file is created in the current document-root folder location, 	and if the file exist then the existing file and content given in the body and same then it sends '204 Not Modified' or 	if the contents are different then it sends '200 OK'
5)DELETE 
	If the user is admin it allows to delete the file and sends '200 OK',and if the file does not exist then '404 Not Found' 	and if the user is not the admin it sends '405 Method Not Allowed'  
6)OPTIONS
	If the user is admin all the options are available and sends 'Allow:GET PUT POST DELETE HEAD OPTIONS' and if the user is 	not admin it sends 'GET POST HEAD OPTIONS ' 

Some commonly encountered status codes are:
200 OK: The request is fulfilled.
304 Not Modified: In response to the If-Modified-Since conditional GET request, the server notifies that the resource requested has not been modified.
400 Bad Request: Server could not interpret or understand the request, probably syntax error in the request message.
404 Not Found: The requested resource cannot be found in the server.
405 Method Not Allowed: The request method used, e.g., POST, PUT, DELETE, is a valid method. However, the server does not allow that method for the resource requested.
501 Method Not Implemented: The request method used is invalid (could be caused by a typing error, e.g., "GET" misspell as "Get").
