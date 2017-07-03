import socket
import sys
import select
import queue

message_queues = {}

HOST = ''                 #The remote host
PORT = 50015              #The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

message_queues[s] = queue.Queue()

inputs_client = [s, sys.stdin]
outputs_client = []

timeout = 1

while inputs_client:
    readable_client, writable_client, exceptional_client = select.select(
        inputs_client, outputs_client, inputs_client, timeout)
    
    #if not (readable_client or writable_client or exceptional_client):
        #continue
    for item in readable_client:

        if item is not sys.stdin:
            #inp = sys.stdin.readlines()
            data = item.recv(1024)
            if data:
                # A readable client socket has data
                print('Friend:{!r}'.format(data, item.getpeername()))
                #message_queues[item].put(data)
                # Add output channel for response
                #if item not in outputs_client:
                #    outputs_client.append(item)
            else:
                # Interpret empty result as closed connection
                print('closing')
                # Stop listening for input on the connection
                #if item in outputs_client:
                #    outputs_client.remove(item)
                #inputs_client.remove(item)
                item.close()
                # Remove message queue  
                del message_queues[item]
                
        else:
            inp = sys.stdin.readline()
            #item.send(inp)
            #print "sent"
            socket_list = message_queues.keys()
            for sock in socket_list:
                message_queues[sock].put(inp)
                if sock not in outputs_client:
                    outputs_client.append(sock)
        
    for item in writable_client:
        try:
            next_msg = message_queues[item].get_nowait()
        except queue.Empty:
            #print("Queue empty")
            outputs_client.remove(item)
        else:
            #print('  sending {!r} to {}'.format(next_msg,
            #                                    item.getpeername()))
            item.send(next_msg)    
    
    for item in exceptional_client:
        print('exception condition on', item.getpeername())
        # Stop listening for input on the connection
        inputs_client.remove(item)
        if item in outputs_client:
            outputs_client.remove(item)
            item.close()
        # Remove message queue
        del message_queues[item]


# message = raw_input("-->>")

# while message != "Bye":
   
#    s.send(message)
#    data = s.recv(1024)
#    print data
#    #print 'Recieved-->', repr(data)
#    message = raw_input("-->>")
# s.close()
