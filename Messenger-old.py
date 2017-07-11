import socket 
import select
import sys
import queue

from string import printable
from curses import erasechar, wrapper

#Terminal input change
printable = map(ord, printable)

def socketInfo(HOST, PORT)
    PORT = 50019  
    HOST = '127.0.0.1'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)

    inputs = [s, sys.stdin]
    outputs = []
    message_queues = {}
    timeout = 1

#Functions being defined 
def interpretData(item, message_queues):
    data = item.recv(1024)
    if data:
       # A readable client socket has data
       print('Friend:{!r}'.format(data, item.getpeername()))    
    else:
       # Interpret empty result as closed connection
       print('closing', server_address)
       inputs.remove(item)
       item.close()
       #Remove message queue  
       del message_queues[item]

def inputData(stdscr): 
    #inp = sys.stdin.readline()
    #print type(inp)
    
    socket_list = message_queues.keys()
    Y,X = stdscr.getyx()
    #rawInputs = []
    inpString = []
    while True:
        inpChar = stdscr.getch()
        if inpChar in (13, 10):
            break
        elif inpChar == 263:
            y, x = stdscr.getyx
            if x > X:
                del inpChar[-1]
                stdscr.move(y, (x-1))
                stdscr.clrtoeol()
                stdscr.refresh()
        elif inpChar in printable:
             inpString.append(chr(inpChar))
             stdscr.addch(inpChar)
    inp = "".join(inpString)
    #print inp
    #print type(inp)
    #return inp
    #print inp
    for sock in socket_list:
        message_queues[sock].put(inp)
        if sock not in outputs:
            outputs.append(sock)


def prompt(stdscr, y, x, prompt = ">>>"):
    stdscr.move(y, x)
    stdscr.clrtoeol()
    stdscr.addstr(y, x, prompt)
    return inputData(stdscr)



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

#Messenger Server Function -- 
def messengerServer():
    
    print('starting up on {} port {}'.format(*server_address))
    
    s.setblocking(0)
    s.bind((HOST, PORT))
    s.listen(5) 

    print "Welcome to Jchat! You can now start sending messages!"
    #sys.stdout.write('[Me] '); sys.stdout.flush()
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
                interpretData(item, message_queues)
                
            else:
                inputData(item, message_queues)

        for item in writable:
            writingFunc(item)   
                                                  
        for item in exceptional:
            exceptionalFunc(item)

#Client function -- 
def messengerClient():
    s.connect((HOST, PORT))

    message_queues[s] = queue.Queue()
    
    print "Welcome to Jchat! You can now start sending messages!"
    sys.stdout.write('[Me] '); sys.stdout.flush()
    while inputs:
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs, timeout)
        
        if not (readable or writable or exceptional):
            continue
        for item in readable:

            if item is not sys.stdin:
                interpretData(item, message_queues)
                    
            else:
                inputData(item, message_queues)
            
        for item in writable:
            writingFunc(item)    
        
        for item in exceptional:
            exceptionalFunc(item)
#wrapper(display)
def main(stdscr):
    Y, X = stdscr.getmaxyx()
    lines = []
    max_lines = (Y - 3)
    stdscr.clear()
    stdscr.addstr("Welcome to Jchat")
    while True:
        inpString = prompt(stdscr, (Y - 1), 0)
        if inpString == "Bye":
            break
        #scrolling

        if len(lines) > max_lines:
            lines = lines[1:]
            stdscr.clear()
            for i, line in enumerate(lines):
                stdscr.addstr(i, 0, line)

        stdscr.addstr(len(lines), 0, inpString)
        lines.append(inpString)

        stdscr.refresh()

if __name__ == "__main__":
    #wrapper(main)
    if sys.argv[1] == "server":
        messengerServer()
    else:
        messengerClient()
    

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