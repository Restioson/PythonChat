#Imports
import Tkinter
import socket
import threading

#Tkinter
root = Tkinter.Tk()
root.title("Socket console")

#Sockets
sock = socket.socket()
sock.bind(("0.0.0.0", 7000))
client_sock = None

#Sends data
def callback():
    try:
        client_sock.send("[Server] ".encode("utf-8") + send_data.get().encode("utf-8"))
        send_data.delete(0, 'end')
    except: pass

#Console widget
console = Tkinter.Text(root)
console.config(state=Tkinter.DISABLED)
console.pack()

#Entry widget
send_data = Tkinter.Entry(root)
send_data.pack()

#Send button
send = Tkinter.Button(root, text="Send", command=callback)
send.pack()

#Listens for data
def listener(s):
    while 1:
        d = s.recv(1024*1024)
        console.config(state=Tkinter.NORMAL)
        console.insert(Tkinter.END, str(d) + "\n")
        console.config(state=Tkinter.DISABLED)

#Listens for connections
def listen_for_connections():
    global client_sock
    while 1:
        sock.listen(1)
        client_sock, addr = sock.accept()
        socket_listener_thread = threading.Thread(target=listener, args=(client_sock,))
        socket_listener_thread.daemon = True
        socket_listener_thread.start()
    
#Starts connection thread
listen_thread = threading.Thread(target=listen_for_connections)
listen_thread.daemon = True
listen_thread.start()

root.mainloop()
