import socket 
import select
import sys
import queue

#conn, addr = item.accept()

#print 'Connected by', addr
#data = raw_input('Lets chat!-->')

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
PORT = 50017  
HOST = '127.0.0.1'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)

inputs = [s, sys.stdin]
outputs = []
message_queues = {}
timeout = 1

def messengerServer():
    

    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('starting up on {} port {}'.format(*server_address))
    
    s.setblocking(0)
    s.bind((HOST, PORT))
    s.listen(5) 
    #timeout = 1
    
    #inputs = [s, sys.stdin]
    #outputs = []
    #message_queues = {}
    print "Welcome to Jchat! You can now start sending messages!"
    sys.stdout.write('[Me] '); sys.stdout.flush()
    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)

        if not (readable or writable or exceptional):
            #print('  timed out, do some other work here')
            continue
        for item in readable:
            if item is s:
                conn, addr = item.accept()
                print 'Connected by', addr
                conn.setblocking(0)
                inputs.append(conn)
                message_queues[conn] = queue.Queue()
                
            elif item is not sys.stdin:
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
                
            else:
                #inp = sys.stdin.write('[Me]:')
                #sys.stdout.write('[Me]') + inp 
                inp = sys.stdin.readline()
                socket_list = message_queues.keys()
                for sock in socket_list:
                    message_queues[sock].put(inp)
                    if sock not in outputs:
                        outputs.append(sock)

        for item in writable:
            try:
                next_msg = message_queues[item].get_nowait()
            except queue.Empty:
                outputs.remove(item)
            else:
                item.send(next_msg)  
                sys.stdout.write('[Me] '); sys.stdout.flush()   
                                                  
        for item in exceptional:
            print('exception condition on', item.getpeername())
            # Stop listening for input on the connection
            inputs.remove(item)
            if item in outputs:
                outputs.remove(item)
            item.close()
            # Remove message queue
            del message_queues[item]

def messengerClient():
    #message_queues = {}

    #HOST = ''                 #The remote host
    #PORT = 50015              #The same port as used by the server
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    message_queues[s] = queue.Queue()

    #inputs = [s, sys.stdin]
    #outputs = []

    #timeout = 1
    print "Welcome to Jchat! You can now start sending messages!"
    sys.stdout.write('[Me] '); sys.stdout.flush()
    while inputs:
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs, timeout)
        
        if not (readable or writable or exceptional):
            continue
        for item in readable:

            if item is not sys.stdin:
                data = item.recv(1024)
                if data:
                    # A readable client socket has data
                    print('Friend:{!r}'.format(data, item.getpeername()))
                else:
                    # Interpret empty result as closed connection
                    print('closing')
                    inputs.remove(item)
                    item.close()
                    # Remove message queue  
                    del message_queues[item]
                    
            else:
                #sys.stdin.write('[Me] '); sys.stdout.flush()
                inp = sys.stdin.readline(); sys.stdout.flush()
                
                socket_list = message_queues.keys()
                for sock in socket_list:
                    message_queues[sock].put(inp)
                    if sock not in outputs:
                        outputs.append(sock)
            
        for item in writable:
            try:
                next_msg = message_queues[item].get_nowait()
            except queue.Empty:
                outputs.remove(item)
            else:
                item.send(next_msg)
                sys.stdout.write('[Me] '); sys.stdout.flush()    
        
        for item in exceptional:
            print('exception condition on', item.getpeername())
            # Stop listening for input on the connection
            inputs.remove(item)
            if item in outputs:
                outputs.remove(item)
                item.close()
            # Remove message queue
            del message_queues[item]

if __name__ == "__main__":
    if sys.argv[1] == "server":
        messengerServer()
    else:
        messengerClient()
    

