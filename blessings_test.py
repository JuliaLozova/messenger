import socket 
import select
import sys
import queue
import os
import signal
from blessings import Terminal
from blessed import Terminal

term = Terminal()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

PORT = 50210

inputs = [sock, sys.stdin]
outputs = []
message_queues = {}
timeout = 0.01

term = Terminal()

def recieveMessage(item, message_queues):
    data = item.recv(1024)
    if data:
       # A readable client socket has data
        with term.location(0, (term.height - 1)):
            print 'Friend: '+ format(data),
        refresh_input_line()
    else:
       # Interpret empty result as closed connection
       print('closing')
       inputs.remove(item)
       item.close()
       #Remove message queue  
       del message_queues[item]

def readAndPrintStdin(item, message_queues):
    inp = sys.stdin.readline()

    refresh_input_line()
    socket_list = message_queues.keys()
    for sock in socket_list:
        message_queues[sock].put(inp)
        if sock not in outputs:
            outputs.append(sock)

    #return outputs
def sendMessage(item):
    try:
        next_msg = message_queues[item].get_nowait()
    except queue.Empty:
        outputs.remove(item)
    else:
        item.send(next_msg)
        

def handleErrors(item):
    print('exception condition on', item.getpeername())
    
    # Stop listening for input on the connection
    inputs.remove(item)
    if item in outputs:
        outputs.remove(item)
        item.close()
    # Remove message queue
    del message_queues[item]

def handleBuffers(isServer):
    readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)
    if not (readable or writable or exceptional):
        return

    for item in readable:
        
        if item is sock and isServer:
            conn, addr = item.accept()
            with term.location(0, (term.height - 2)):
                print 'Client connected ', addr
            refresh_input_line()
            conn.setblocking(0)
            inputs.append(conn)
            message_queues[conn] = queue.Queue()

        elif item is sys.stdin:
            readAndPrintStdin(item, message_queues)
        else:
            recieveMessage(item, message_queues)
    for item in writable:
        sendMessage(item)   
                                                
    for item in exceptional:
        handleErrors(item)

def getIPaddress():
    return ([(sock.connect(('8.8.8.8', 53)), sock.getsockname()[0], sock.close()) for sock in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])

def startServer():
    server_address = (getIPaddress(), PORT)
    with term.location(0, (term.height - 2)):
        print('Starting server @ {}:{}'.format(*server_address))

    sock.setblocking(0)
    binder = sock.bind(server_address)
    sock.listen(5) 
    

def connectAsClient():
    connected = sock.connect((friendIP, PORT))
    print "Connected as Client"
    message_queues[sock] = queue.Queue()

def chooseClientOrServer():
    isServer = False
    try:
        connectAsClient()
        
    except Exception as e: 
        #print("something'sock wrong with %sock:%d. Exception is %sock" % (HOST, PORT, e))
        startServer()
        isServer = True
    
    with term.location(0, (term.height - 1)):
        print "Welcome to Jchat! You can now start sending messages!"
    
    return isServer

def refresh_input_line():
    with term.location(0, term.height - 1):
        print "ME: ",
    print term.move(term.height - 1, 4),

def signal_handler(signal, frame):
    sock.shutdown()
    sock.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    friendIP = sys.argv[1]
    with term.hidden_cursor(), term.fullscreen():
        isServer = chooseClientOrServer()
        refresh_input_line()
        while inputs:
            handleBuffers(isServer)
