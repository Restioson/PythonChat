import Tkinter
import socket
import sys
import threading
import traceback

def sendMessage():
    try:
        send(inputBox.get())
        inputBox.delete(0, 'end')
    except:
        printConsole('Failed to send message')
        printConsole(traceback.format_exc())
        pass

def printConsole(printMessage):
    console.config(state=Tkinter.NORMAL)
    console.insert(Tkinter.END, printMessage + '\n')
    console.config(state=Tkinter.DISABLED)
    print(printMessage)
    
def send(message):
	client.sendall('[' + name + '] ' + message)

def startClient():
    printConsole('Connecting to server...')
    try:
        client.connect((host, port))
        send('Connected')

        while 1:
            received = client.recv(1024)
            if not received:
                printConsole('Server closed.')
                break
            printConsole(received)
    except:
        printConsole('Failed to connect to server')
        printConsole(traceback.format_exc())
        sys.exit()

name = raw_input("Please enter your name \n")
host = raw_input("Please enter the server host\n")
port = int(raw_input("Please enter the server port\n"))
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

root = Tkinter.Tk()
root.title("Socket Client - GUI")
console = Tkinter.Text(root)
console.config(state=Tkinter.DISABLED)
console.pack()

inputBox = Tkinter.Entry(root)
inputBox.pack()

sendButton = Tkinter.Button(root, text="Send", command=sendMessage)
sendButton.pack()

socketThread = threading.Thread(target=startClient)
socketThread.daemon = True
socketThread.start()

root.mainloop()
