import socket

HOST = ''                 #The remote host
PORT = 50004              #The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

message = raw_input("-->>")

while message != "Bye":
    
    s.send(message)
    data = s.recv(1024)
    print data
    print 'Recieved-->', repr(data)
    message = raw_input("-->>")
s.close()
x