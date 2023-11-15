import tkinter as tk
from time import sleep
import socket
import threading
import random

host = '192.168.48.84'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, 69))
win = tk.Tk()
messageLog = tk.Label(win, text="", anchor='sw')
msgBox = tk.Entry(win)
win.configure()

messageLog.grid(column=1, row=0)
msgBox.grid(column=1, row=1)

msgBox.configure(bg="gray")
messageLog.configure(height=10)

def addMessage(message, host):
    current = messageLog.cget("text")
    if len(current.split("\n")) >= 10:
        newText ="\n".join(current.split("\n")[1:])
        messageLog.configure(text=newText)
    current = messageLog.cget("text")
    newText = current + "\n" + host + message
    messageLog.configure(text=newText)


def keydown(e):
    for event in str(e).split(" "):
        if event[:7].lower() == "keysym=":
            if event[7:].lower() == "return" and msgBox.get() != "":
                splitIntoLines(msgBox.get().split(" "), socket.gethostname())
                s.send(msgBox.get().encode())
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
        msg = s.recv(1024).decode()
        splitIntoLines(msg.split(" "), socket.gethostbyaddr(host)[0])

win.bind("<KeyPress>", keydown)
x = threading.Thread(target=listen)
x.start()
win.mainloop()

        
        


