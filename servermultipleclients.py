# coding utf-8
#Imports
import socket
import threading
import traceback

#Sockets
sock = socket.socket()
sock.bind(("0.0.0.0", 7000))
client_socks = []

#Broadcast
def broadcast(data):
    for sock in client_socks:
        try: sock.sendall(data.encode("utf-8"))
        except: 
            print(traceback.format_exc())
            print("Error. Assuming socket dropped")
            client_socks.remove(sock)

#Listens for data
def listener(s):
    while 1:
        try:
            data = s.recv(1024*1024)
            print(data)
            broadcast(data)
        except:
            print(traceback.format_exc())
            print("Error. Assuming client dropped")
            client_socks.remove(s)

#Listens for connections
def listen_for_connections():
    while 1:
        print("Listening for connections")
        sock.listen(1)
        client_sock, addr = sock.accept()
        socket_listener_thread = threading.Thread(target=listener, args=(client_sock,))
        socket_listener_thread.daemon = True
        socket_listener_thread.start()
        client_socks.append(client_sock)
    
#Starts connection thread
listen_thread = threading.Thread(target=listen_for_connections)
listen_thread.daemon = True
listen_thread.start()


while 1: pass
