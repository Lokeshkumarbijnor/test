#!Python/python.exe

print("Content-type:text/html\r\n\r\n")
# Import modules for CGI handling 
import cgi, cgitb

# Create instance of FieldStorage 
data= cgi.FieldStorage()

# Get data from fields
output = data.getvalue("param")

# This will print to stdout for testing
print("Hello World!!!")
print(output)