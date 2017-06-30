import random
import socket 

HOST = ''                 
PORT = 50007              
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))

s.listen(1)
conn, addr = s.accept()

print 'Connected by', addr
data = raw_input('Lets chat!-->')

while 1:
    data = conn.recv(1024)
    if not data: break
    
    print data
    print 'Recieved-->', repr(data)
    data = raw_input("-->")
    conn.send(data)
conn.close()

