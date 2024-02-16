import socket, threading, os, queue
from user import User

#Server Code
def recv(sock, recvPackets):
    while True:
        data,addr = sock.recvfrom(1024)
        recvPackets.put((data,addr))

def serv():
    host = socket.gethostbyname(socket.gethostname())
    port = 5000
    print('Server hosting on IP-> '+str(host))
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))
    clients = set()
    usernames = set()
    recvPackets = queue.Queue()
    welcome = 'Welcome to server ' + host + ' '

    print('Server Running...')

    threading.Thread(target=recv,args=(s,recvPackets)).start()

    while True:
        while not recvPackets.empty():
            # received packet
            data, addr = recvPackets.get()

            # keeps track of all connected clients
            tmpaddr = []
            for a in usernames:
                tmpaddr.append(a.client)

            data = data.decode('utf-8')
            # test to see if received client info is not already stored
            if addr not in tmpaddr:
                # new address
                u = User(data, addr)
                usernames.add(u)

                # welcome message
                tmp = welcome + u.username + '!'
                s.sendto(tmp.encode('utf-8'), u.client)
                broadcast(u.username + ' has joined!', usernames, s, addr)
                print(u.username + ' joined server')
                continue
                # there was an add here
            if data.endswith('!exit'):
                for u in usernames.copy():         # remove client
                    if u.client == addr:
                        print('removing ', u)
                        usernames.remove(u)
                        broadcast(u.username + ' has left', usernames, s, addr)
                continue
            if data.endswith('!all'):
                tmp = ''
                for u in usernames:
                    tmp += u.username + ' '
                # broadcast
                for u in usernames:
                    s.sendto(tmp.encode('utf-8'), u.client)
            print(str(addr)+data)
            # send message to all clients except one who sent
            for u in usernames:
                s.sendto(data.encode('utf-8'), u.client)
    print('closed')
    s.close()
#Server Code Ends Here

'''
    sends message to all users
'''
def broadcast(message, users, sock, address):
    for u in users:
        if u.client != address:
            sock.sendto(message.encode('utf-8'), u.client)

if __name__ == '__main__':
    try:
        serv()
    except KeyboardInterrupt:
        print('\nbye')
        os._exit(0)