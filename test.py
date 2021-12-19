#!C:\Python\python.exe

print('content-type: text/html\r\n\r\n')
import cgi,os

form = cgi.FieldStorage()
msg = form.getvalue("message_py")
print ('<html>')
print ('<head>')
print ('<title>Hello World - First CGI Program</title>')
print ('</head>')
print ('<body>')
print ('<h2>Hello World! This is my first CGI program %s</h2>'% msg)
print ('</body>')
print ('</html>')
