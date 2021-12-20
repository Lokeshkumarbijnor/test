#!C:/Python/python
print('Content-type: text/html\r\n\r\n')
import cgi
data= cgi.FieldStorage()
#Get data from fields
output = data.getvalue("param")
print(f"<p>{output}</p>")