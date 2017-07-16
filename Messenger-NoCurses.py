import socket 
import select
import sys
import queue
import os

PORT = 50016  
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

inputs = [sock, sys.stdin]
outputs = []
message_queues = {}
timeout = 1

def recieveMessage(item, message_queues):
    data = item.recv(1024)
    if data:
       # A readable client socket has data
       print('Friend:{!r}'.format(data, item.getpeername()))    
    else:
       # Interpret empty result as closed connection
       print('closing', addr)
       inputs.remove(item)
       item.close()
       #Remove message queue  
       del message_queues[item]

def readStdin(item, message_queues):
    inp = sys.stdin.readline()
    socket_list = message_queues.keys()
    for sock in socket_list:
        message_queues[sock].put(inp)
        if sock not in outputs:
            outputs.append(sock)

def displayStdin(item):
    try:
        next_msg = message_queues[item].get_nowait()
    except queue.Empty:
        outputs.remove(item)
    else:
        item.send(next_msg)  
        sys.stdout.write('[Me] '); sys.stdout.flush() 

def handleErrors(item):
    print('exception condition on', item.getpeername())
    
    # Stop listening for input on the connection
    inputs.remove(item)
    if item in outputs:
        outputs.remove(item)
        item.close()
    # Remove message queue
    del message_queues[item]

def handleMessages(makeConnection):
    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)
        if not (readable or writable or exceptional):
            #print('  timed out, do some other work here')
            continue

        for item in readable:
            
            if item is sock and acceptConnection:
                conn, addr = item.accept()
                print 'Connected by', addr
                conn.setblocking(0)
                inputs.append(conn)
                message_queues[conn] = queue.Queue()

            elif item is sys.stdin:
                readStdin(item, message_queues)
            else:
                recieveMessage(item, message_queues)
        for item in writable:
            displayStdin(item)   
                                                  
        for item in exceptional:
            handleErrors(item)

def messengerServer():
    server_address = (getIPaddress(), PORT)
    print('starting up on {} port {}'.format(*server_address))

    sock.setblocking(0)
    binder = sock.bind(server_address)
    sock.listen(5) 

    print "Welcome to Jchat! You can now start sending messages!"
    sys.stdout.write('[Me] '); sys.stdout.flush()
    
    acceptConnection = True
    handleMessages(acceptConnection)

def messengerClient():
    connected = sock.connect((friendIP, PORT))
    message_queues[sock] = queue.Queue()
    
    print "Welcome to Jchat! You can now start sending messages!"
    sys.stdout.write('[Me] '); sys.stdout.flush()
    
    acceptConnection = False
    handleMessages(acceptConnection)

def getIPaddress():
    return ([(sock.connect(('8.8.8.8', 53)), sock.getsockname()[0], sock.close()) for sock in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])

def chooseClientOrServer():
    try:
        messengerClient() 
    except Exception as e: 
        #print("something'sock wrong with %sock:%d. Exception is %sock" % (HOST, PORT, e))
        messengerServer()

if __name__ == "__main__":
    friendIP = sys.argv[1]
    chooseClientOrServer()
    
# def select.select(inputs, outputs, error_bufs):
#     readable = []
#     writable = []
#     exceptional = []
#     for input in inputs:
#         if input.hasData():
#             readable.append(input)
#     for output in outputs:
#         if output.hasSpace():
#             writable.append(output)
#     for buf in error_bufs:
#         if buf.hasErrors():
#             exceptional.append(buf)
    
#     return readable, writable, exceptional