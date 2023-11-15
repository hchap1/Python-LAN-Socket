import tkinter as tk
from time import sleep
import socket
import threading
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.48.84', 69))
s.listen()
client, addr = s.accept()
win = tk.Tk()
messageLog = tk.Label(win, text="\n\n\n\n\n\n\n\n\n\n")
prompt = tk.Label(win, text="MSG:")
msgBox = tk.Entry(win)

messageLog.grid(column=1, row=0)
prompt.grid(column=0, row=1)
msgBox.grid(column=1, row=1)

def addMessage(message, host):
    current = messageLog.cget("text")
    if len(current.split("\n")) >= 10:
        newText ="\n".join(current.split("\n")[1:])
        messageLog.configure(text=newText)
    current = messageLog.cget("text")
    newText = current + "\n" + host + message
    messageLog.configure(text=newText)

def keydown(e):
    stringE = str(e).split(" ")
    for event in stringE:
        if event[:7] == "keysym=":
            if event[7:].lower() == "return" and msgBox.get() != "":
                splitIntoLines(msgBox.get().split(" "), socket.gethostname())
                client.send(msgBox.get().encode())
                msgBox.delete(0,len(msgBox.get()))

def splitIntoLines(words, hostName):
    iteration = 0
    if len(words) >= 5:
        while True:
            try:
                myList = []
                for i in range(5):
                    myList.append(words[i])
                words = words[5:]
                if iteration == 0:
                    addMessage(" ".join(myList), hostName + ": ")
                else:
                    addMessage(" ".join(myList), "")
            except:
                addMessage(" ".join(words), "")
                break
            iteration += 1 
    else:
        addMessage(" ".join(words), hostName + ": ")

def listen():
    while True:
        msg = client.recv(1024).decode()
        splitIntoLines(msg.split(" "), socket.gethostbyaddr(addr[0])[0])

win.bind("<KeyPress>", keydown)
x = threading.Thread(target=listen)
x.start()
win.mainloop()

        
        



