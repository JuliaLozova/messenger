import random
import socket 

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))

s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(1024)
    if not data: break
    conn.sendall(data)
conn.close()
#
#answers = [
#    "Hello Stranger",
#    "Its been a while",
#    "Awesome",
#    "YAY!"
#]
#
#print("Welcome to Jchat")
#print("Say 'Bye' to end chat")
#userInput = raw_input("Let's Chat!\n")
#while userInput != "Bye":
#    print random.choice(answers)
#    userInput = raw_input("")
#
