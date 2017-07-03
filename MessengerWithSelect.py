import socket 
import select
import sys
import queue

PORT = 50015  
HOST = '127.0.0.1'                 
server_address = (HOST, PORT)            


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

def messengerServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('starting up on {} port {}'.format(*server_address))
    
    s.setblocking(0)
    s.bind((HOST, PORT))
    s.listen(5) 
    timeout = 1
    
    inputs = [s, sys.stdin]
    outputs = []
    message_queues = {}

    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)

        if not (readable or writable or exceptional):
            #print('  timed out, do some other work here')
            continue
        for item in readable:
            if item is s:
                conn, addr = item.accept()
                #print conn
                print 'Connected by', addr
                conn.setblocking(0)
                inputs.append(conn)
                message_queues[conn] = queue.Queue()
                #print type(conn)
                #print message_queues
            elif item is not sys.stdin:
                data = item.recv(1024)
                if data:
                    # A readable client socket has data
                    print('[Friend:' + str(item.getpeername()) + str(data))
                    #message_queues[item].put(data)
                    # Add output channel for response
                    #if item not in outputs:
                        #outputs.append(item)
                else:
                    # Interpret empty result as closed connection
                    print('closing', addr)
                    # Stop listening for input on the connection
                    #if item in outputs:
                    #    outputs.remove(item)
                    #inputs.remove(item)
                    item.close()
                    #Remove message queue  
                    del message_queues[item]
                
            else:
                inp = sys.stdin.readline()
                #print "Sending at else"
                #item.send(inp)
                socket_list = message_queues.keys()
                for sock in socket_list:
                    message_queues[sock].put(inp)
                    #print next_msg
                    #item.send(next_msg)
                    if sock not in outputs:
                        outputs.append(sock)

                        #print sock
                #message_queues[].put(inp)
                #if inp not in outputs:
                #    outputs.append(inp)


        for item in writable:
            try:
                next_msg = message_queues[item].get_nowait()
                #item.send(next_msg)
                #print "Sending messages"
                #item.send(next_msg)
            
            except queue.Empty:
                outputs.remove(item)
                #print('  sending {!r} to {}'.format(next_msg,item.getpeername()))
            else:
                item.send(next_msg)    
                                                  
        
        for item in exceptional:
            print('exception condition on', item.getpeername())
            # Stop listening for input on the connection
            inputs.remove(item)
            if item in outputs:
                outputs.remove(item)
            item.close()
            # Remove message queue
            del message_queues[item]

#def messengerClient():
#    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    s.connect((HOST, PORT))
#
#    while 1:
#        socket_list = message_queues.keys()
#        for sock in socket_list:
#            if sock == s:
#
#            message_queues[sock].put(inp)
#            if sock not in outputs:
#                outputs.append(sock)
    #while message != "Bye":
    #
    #    s.send(message)
    #    data = s.recv(1024)
    #    print data
    #    print 'Recieved-->', repr(data)
    #    message = raw_input("-->>")
    #s.close()

if __name__ == "__main__":
    messengerServer()
    #s.close()

