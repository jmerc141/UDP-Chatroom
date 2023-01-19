# receiver
import socket, select
from pickle import loads

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = extract_ip()
print(ip)
port = 5005
timeout = 3
sock.bind((ip, port))

while True:
	data, addr = sock.recvfrom(1024)
	if data:
		d = loads(data)
		print('File name:', d)
		fname = d.strip()
		print(fname)

	#f = open(fname, 'wb')

	