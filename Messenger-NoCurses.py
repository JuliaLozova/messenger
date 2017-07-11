import socket 
import select
import sys
import queue
import os
#hostname = "google.com" #example



PORT = 50019  
HOST = '127.0.0.1'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
#result = s.connect_ex((HOST,PORT))
#connected = s.connect((HOST, PORT))
#response = os.system("ping -c 1 " + HOST)
#print "other r"
#print response

inputs = [s, sys.stdin]
outputs = []
message_queues = {}
timeout = 1

def interpretData(item, message_queues):
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

def inputData(item, message_queues):
    inp = sys.stdin.readline()
    socket_list = message_queues.keys()
    for sock in socket_list:
        message_queues[sock].put(inp)
        if sock not in outputs:
            outputs.append(sock)

def writingFunc(item):
    try:
        next_msg = message_queues[item].get_nowait()
    except queue.Empty:
        outputs.remove(item)
    else:
        item.send(next_msg)  
        sys.stdout.write('[Me] '); sys.stdout.flush() 

def exceptionalFunc(item):
    print('exception condition on', item.getpeername())
    
    # Stop listening for input on the connection
    inputs.remove(item)
    if item in outputs:
        outputs.remove(item)
        item.close()
    # Remove message queue
    del message_queues[item]

def manyFunctions(makeConnection):
    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)
        if not (readable or writable or exceptional):
            #print('  timed out, do some other work here')
            continue

        for item in readable:
            
            if item is s and makeConnection == 1:
                conn, addr = item.accept()
                print 'Connected by', addr
                conn.setblocking(0)
                inputs.append(conn)
                message_queues[conn] = queue.Queue()

            elif item is not sys.stdin:
                interpretData(item, message_queues)
                
            else:
                inputData(item, message_queues)
        for item in writable:
            writingFunc(item)   
                                                  
        for item in exceptional:
            exceptionalFunc(item)

def messengerServer():
    
    print('starting up on {} port {}'.format(*server_address))
    
    s.setblocking(0)
    #binder = s.bind((HOST, PORT))
    s.listen(5) 
    print "here is bind"
    #s.bind((HOST,PORT))
    print binder
    print server_address
    print "Welcome to Jchat! You can now start sending messages!"
    sys.stdout.write('[Me] '); sys.stdout.flush()
    
    makeConnection = 1
    manyFunctions(makeConnection)

def messengerClient():
    #s.connect((HOST, PORT))

    connected = s.connect((HOST, PORT))
    print "this is connected:"
    print connected
    
    message_queues[s] = queue.Queue()
    
    print "Welcome to Jchat! You can now start sending messages!"
    sys.stdout.write('[Me] '); sys.stdout.flush()
    
    makeConnection = 0
    manyFunctions(makeConnection)

def doesServerExist(PORT):
    #print response
    #print "server Response"
    #response = os.system("ping -c 1 " + HOST)
    #print response
    #
    #if response == 0:
    #    messengerServer()
    #    print "port open"
    #else:
    #    #messengerClient()
    #    print "port closed"
    while True:
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((HOST, PORT))
        except OSError as e:
            if e.errno is 98: ## Errorno 98 means address already bound
                return True
            raise e
        s.close()
        return False

if __name__ == "__main__":
    #connected = s.connect((HOST, PORT))
    #connected = 0
    #ret = os.system("ping -c 1 " + HOST)
    #doesServerExist()
    b = doesServerExist(PORT)
    print("Is port {0} open {1}".format(PORT,b))
    
    #if result == 0:
    #    print "Port is open"
    #else:
    #    print "Port is not open"
    #if ret != 0:
    #    print "Host is not up"
    #else:
    #    print "Hose is up"
        
    if sys.argv[1] == "server":
        messengerServer()
    else:
        messengerClient()
    

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