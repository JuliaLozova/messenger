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

PORT = 50629

inputs = [sock, sys.stdin]
outputs = []
message_queues = {}
timeout = 0.01


term = Terminal()

def recieveMessage(item, message_queues, user_map):
    data = item.recv(1024)
    if data:
        user_map[item] = data.split(":")[0]
        # A readable client socket has data
        with term.location(0, (term.height - 1)):
            print format(data),
    else:
        # Interpret empty result as closed connection
        with term.location(0, (term.height - 1)):
            if item in user_map:
                print(user_map[item] + ' has disconnected')
            else:
                print('Friend has disconnected')
        inputs.remove(item)
        item.close()
        # Remove message queue
        del message_queues[item]
    return data


def readAndPrintStdin(inp, message_queues, user_name):
    socket_list = message_queues.keys()
    inp = user_name + ': ' + ''.join(inpList)
    for sock in socket_list:
        message_queues[sock].put(inp)
        if sock not in outputs:
            outputs.append(sock)


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

def handleBuffers(isServer, inpList, user_name, user_map):
    readable, writable, exceptional = select.select(
        inputs, outputs, inputs, timeout)
    if not (readable or writable or exceptional):
        return inpList

    for item in readable:

        if item is sock and isServer:
            conn, addr = item.accept()
            with term.location(0, (term.height - 1)):
                print 'Client connected ', addr

            inputs.append(conn)
            message_queues[conn] = queue.Queue()

        elif item is not sys.stdin:
            msg = recieveMessage(item, message_queues, user_map)
            if isServer:
                socket_list = message_queues.keys()
                for client_sock in socket_list:
                    if client_sock is not item:
                        message_queues[client_sock].put(msg)
                        if client_sock not in outputs:
                            outputs.append(client_sock)
                
    for item in writable:
        sendMessage(item)

    for item in exceptional:
        handleErrors(item)

    val = term.inkey(timeout=0)

    if val:
        inpList.append(str(val))
        inp = ''.join(inpList)

        if ord(val) is 3:
            signal_handler()

        elif val.is_sequence:
            if val.name == "KEY_ENTER":
                inpList.append("\r\n")
                inp = ''.join(inpList)
                with term.location(0, term.height - 1):
                    print "ME: " + inp,
                readAndPrintStdin(inp, message_queues, user_name)
                del inpList[:]

            elif val.name == "KEY_DELETE":
                inpList = inpList[:-2]
                inp = ''.join(inpList)

    return inpList


def getIPaddress():
    return ([(sock.connect(('8.8.8.8', 53)), sock.getsockname()[0], sock.close()) for sock in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])


def startServer():
    server_address = (getIPaddress(), PORT)
    with term.location(0, (term.height - 3)):
        print('Starting server @ {}:{}\n'.format(*server_address))

    sock.setblocking(0)
    binder = sock.bind(server_address)
    sock.listen(5)


def connectAsClient():
    connected = sock.connect((friendIP, PORT))
    with term.location(0, (term.height - 3)):
        print "Connected as Client\n"
    message_queues[sock] = queue.Queue()


def chooseClientOrServer():
    isServer = False
    try:
        connectAsClient()

    except Exception as e:
        startServer()
        isServer = True

    with term.location(0, (term.height - 3)):
        print "Welcome to Jchat! You can now start sending messages!\n"

    return isServer


def refresh_input_line(inpList):
    with term.location(0, term.height - 1):
        out = ": " + ''.join(inpList)
        clearing = ' ' * (term.width - len(out))
        print out + clearing,


def signal_handler(signal='', frame=''):
    sock.shutdown(0)
    sock.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    friendIP = sys.argv[1]
    user_name = raw_input("Enter Username: ")
    with term.hidden_cursor(), term.fullscreen(), term.raw():
        isServer = chooseClientOrServer()
        inpList = []
        user_map = {}

        while inputs:
            inpList = handleBuffers(isServer, inpList, user_name, user_map)
            refresh_input_line(inpList)
