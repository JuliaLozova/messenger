import socket 
import select
import sys
import queue

HOST = ''                 
PORT = 50004  
server_address = ('', 50004)            
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('starting up on {} port {}'.format(*server_address))
s.setblocking(0)

s.bind((HOST, PORT))

s.listen(5)

inputs = [s, sys.stdin]
outputs = []
message_queues = {}
#

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

timeout = 0.01
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
            #inp = sys.stdin.readlines()
            data = item.recv(1024)
            if data:
                # A readable client socket has data
                print('Friend:{!r}'.format(
                    data, item.getpeername()))
                message_queues[item].put(data)
                # Add output channel for response
                if item not in outputs:
                    outputs.append(item)
            else:
                # Interpret empty result as closed connection
                print('  closing', addr)
                # Stop listening for input on the connection
                if item in outputs:
                    outputs.remove(item)
                inputs.remove(item)
                item.close()

                # Remove message queue  
                del message_queues[item]
        
        else:
            inp = sys.stdin.readline()
            socket_list = message_queues.keys()
            for socket in socket_list:
                message_queues[socket].put(inp)
            
                if socket not in outputs:
                    outputs.append(socket)

            #message_queues[].put(inp)
            #if inp not in outputs:
            #    outputs.append(inp)


    for item in writable:
        try:
            next_msg = message_queues[item].get_nowait()
        except queue.Empty:

            #print("Queue empty")
            outputs.remove(item)
        else:
            #print('  sending {!r} to {}'.format(next_msg,
            #                                    item.getpeername()))
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
#while 1:
#    readable, writable = select.select(inputs,outputs) 
#    message_queues[connection] = queue.Queue()                                          
#    data = conn.recv(1024)
#    if data:
#        # A readable client socket has data
#        print('  received {!r} from {}'.format(
#            data, item.getpeername()), file=sys.stderr,
#        )
#        message_queues[item].put(data)
#        # Add output channel for response
#        if item not in outputs:
#            outputs.append(item)
#    
#    if not data: break
#    
#    print data
#    print 'Recieved-->', repr(data)
#    data = raw_input("-->")
#    conn.send(data)
#conn.close()

