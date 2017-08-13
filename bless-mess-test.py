import socket 
import select
import sys
import queue
import os
from blessings import Terminal

def messengerServer():
    server_address = (getIPaddress(), PORT)
    with term.location(0, (term.height / 2)):
    #print 'This is at the bottom.'
        print('starting up on {} port {}'.format(*server_address))

    sock.setblocking(0)
    binder = sock.bind(server_address)
    sock.listen(5) 
    with term.location(0, (term.height / 2)):
        print "Welcome to Jchat! You can now start sending messages!"
    with term.location(0, term.height):
        print '[Me>>>]'
    
    acceptConnection = True
    return handleMessages(acceptConnection)

def messengerClient():
    connected = sock.connect((friendIP, PORT))
    message_queues[sock] = queue.Queue()
    
    with term.location(0, (term.height / 2)):
        print "Welcome to Jchat! You can now start sending messages!"
    with term.location(0, term.height):
        print '[Me>>>!!!!]'
    
    acceptConnection = False
    return handleMessages(acceptConnection)

def getIPaddress():
    return ([(sock.connect(('8.8.8.8', 53)), sock.getsockname()[0], sock.close()) for sock in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])

def chooseClientOrServer():
    try:
        messengerClient() 
    except Exception as e: 
        #print("something'sock wrong with %sock:%d. Exception is %sock" % (HOST, PORT, e))
        messengerServer()

if __name__ == "__main__":

    PORT = 50017  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    inputs = [sock, sys.stdin]
    outputs = []
    message_queues = {}
    timeout = 1

    friendIP = sys.argv[1]
    with term.hidden_cursor(), term.fullscreen():
        while True:
            chooseClientOrServer()
    #chooseClientOrServer()