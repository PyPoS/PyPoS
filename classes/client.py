__author__ = 'ebo'

import socket  # for sockets
import sys  # for exit


def connect_to_server(stock):
    try:
        # create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
        sys.exit()

    print 'Socket Created'

    host = 'localhost'
    port = 8888

    try:
        remote_ip = socket.gethostbyname(host)

    except socket.gaierror:
        # could not resolve
        print 'Hostname could not be resolved. Exiting'
        sys.exit()

    print 'Ip address of ' + host + ' is ' + remote_ip

    # Connect to remote server
    s.connect((remote_ip, port))

    print 'Socket Connected to ' + host + ' on ip ' + remote_ip

    #Send some data to remote server
    message = str(stock)

    try:
        #Set the whole string
        s.sendall(message)
    except socket.error:
        #Send failed
        print 'Send failed'
        sys.exit()

    print 'Message sent successfully'

    reply = s.recv(4096)

    print(reply)
    # close socket connection
    # s.close()