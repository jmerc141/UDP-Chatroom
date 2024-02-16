import socket, random, threading, os
from tkinter import *
from tkinter import ttk

stopping = False

# Client Code
def ReceiveData(sock):
    while not stopping:
        try:
            data, addr = sock.recvfrom(1024)
            txt = data.decode('utf-8')
            #print('\n' + txt + '\n' + name + '> ', end='')
            appen('\n' + txt)
        except:
            pass

def RunClient(serverIP):
    global s, server
    host = socket.gethostbyname(socket.gethostname())
    port = random.randint(6000, 10000)
    connect = 'Client IP ->' + str(host) + ' Port->' + str(port)
    appen(connect)
    server = (str(serverIP), 5000)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    appen('Please write your username: ')
    recv = threading.Thread(target=ReceiveData, args=(s,))
    recv.start()

# Client Code Ends Here

def initc():
    RunClient(socket.gethostbyname(socket.gethostname()))

def appen(text):
    ta.config(state='normal')
    ta.insert('end', text + '\n')
    ta.see('end')
    ta.config(state='disabled')

def getname(ev=None):
    global name
    name = e.get()
    if name == '':
        name = 'Guest' + str(random.randint(1000, 9999))
        print('Your name is: ' + name)

    s.sendto(name.encode('utf-8'), server)          # send name to server
    b.config(command=sub)
    e.bind('<Return>', sub)
    e.delete(0, END)

def sub(ev=None):
    ent = e.get()
    if ent == '!exit':
        cleanup()
    elif ent == '':
        print('empty')
    data = '[' + name + ']' + ' -> ' + ent
    s.sendto(data.encode('utf-8'), server)
    e.delete(0, END)

def cleanup():
    global stopping
    # send exit to server
    fin = name + ': !exit'
    s.sendto(fin.encode('utf-8'), server)
    stopping = True
    s.close()
    root.destroy()
    os._exit(0)

name = ''

root = Tk()
tframe = ttk.Frame(root, padding=10)
bframe = ttk.Frame(root)
root.geometry('400x400')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.resizable(False, False)
root.title(string='chatpy')
root.iconbitmap('chat.ico')

tframe.grid(column=0, row=0, sticky='news')
bframe.grid(column=0, row=1, sticky='news')

ta = Text(tframe)
ta.config(font=30)
e = Entry(bframe, width=25)
b = Button(bframe, text='Submit', command=getname)
e.bind('<Return>', getname)
e.config(font=30)

ta.pack()
e.pack(side=LEFT, padx=10, pady=10)
b.pack(side=RIGHT, padx=10, pady=10)
initc()
root.protocol('WM_DELETE_WINDOW', cleanup)
root.mainloop()
