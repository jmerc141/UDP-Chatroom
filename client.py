import socket, random, threading
from collections import deque


class Connection:

    '''
    Thread that adds received data to the message queue
    '''
    def ReceiveData(self, sock):
        while not self.stopping:
            try:
                data, addr = sock.recvfrom(1024)
                txt = data.decode('utf-8')
                #print('Received:', txt)
                self.message_q.append(txt)
            except:
                pass
        

    '''
    Runs when the client sends a message (submit clicked or <enter>)
    '''
    def sub(self, ent, ev=None):
        if ent == '!exit':
            self.cleanup()
        elif ent == '':
            print('empty')
        data = '[' + self.name + ']' + ': ' + ent
        self.s.sendto(data.encode('utf-8'), self.server)
        #self.e.delete(0, tk.END)


    '''
    Stops thread and closes connections, runs when window is closed or !exit is typed
    '''
    def cleanup(self):
        # send exit to server
        fin = self.name + ': !exit'
        self.stopping = True
        try:
            self.s.sendto(fin.encode('utf-8'), self.server)
            self.s.close()
        except NameError as n:
            print('Exited before connecting...')
            print(n)
        


    '''
    Setup connection to server and start listening thread
    '''
    def __init__(self, serverIP: str, username: str):
        self.message_q = deque()
        self.stopping = False
        self.name = username
        if self.name == '':
            self.name = 'Guest' + str(random.randint(0, 9999))
            #print('Your name is: ' + name)
        try:
            #host = socket.gethostbyname(socket.gethostname())
            self.port = random.randint(6000, 10000)
            self.server = (str(serverIP), 5000)
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.bind((serverIP, self.port))
            self.s.sendto(self.name.encode('utf-8'), self.server)
        except OSError as o:
            raise
        
        recv = threading.Thread(target=self.ReceiveData, args=(self.s,))
        recv.daemon = True
        recv.start()
        


