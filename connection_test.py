import socket

try:
    connection = socket.gethostbyaddr('172.17.0.1')
    print('Connection')
except socket.herror:
    print ("Unknown host")