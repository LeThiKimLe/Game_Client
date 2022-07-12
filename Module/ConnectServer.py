import socket
import os


REQUEST={'GET_DATA':1, 'LOGIN':2, 'REGIS':3, 'SAVE':4, 'RANK':5}

class Buffer:
    def __init__(self,s):
        '''Buffer a pre-created socket.
        '''
        self.sock = s
        self.buffer = b''

    def get_bytes(self,n):
        '''Read exactly n bytes from the buffered socket.
           Return remaining buffer if <n bytes remain and socket closes.
        '''
        while len(self.buffer) < n:
            data = self.sock.recv(1024)
            if not data:
                data = self.buffer
                self.buffer = b''
                return data
            self.buffer += data
        # split off the message bytes from the buffer.
        data,self.buffer = self.buffer[:n],self.buffer[n:]
        return data

    def put_bytes(self,data):
        self.sock.sendall(data)

    def get_utf8(self):
        '''Read a null-terminated UTF8 data string and decode it.
           Return an empty string if the socket closes before receiving a null.
        '''
        while b'\x00' not in self.buffer:
            data = self.sock.recv(1024)
            if not data:
                return ''
            self.buffer += data
        # split off the string from the buffer.
        data,_,self.buffer = self.buffer.partition(b'\x00')
        return data.decode()

    def put_utf8(self,s):
        if '\x00' in s:
            raise ValueError('string contains delimiter(null)')
        self.sock.sendall(s.encode() + b'\x00')


def Request_Server(request, infor=None):

    ClientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    hostname='DESKTOP-SH243I1'
    host=socket.gethostbyname(hostname)
    port = 1233

    try:
        ClientSocket.connect((host, port))
    except socket.error as e:
        print(str(e))

    if request=='GET_DATA':
        return Request_GetData(ClientSocket)
    
    if request=='LOGIN':
        return Request_Login(ClientSocket, infor)

    if request=='REGIS':
        return Request_Regis(ClientSocket, infor)

    if request== 'SAVE':
        return Request_SaveResult(ClientSocket, infor)

    if request== 'RANK':
        return Request_GetData(ClientSocket)


def Request_Login(ClientSocket, infor):

    infor.insert(0, 'LOGIN')
    infor=','.join(infor)

    rep=''
    while True:
        try:
            ClientSocket.send(str.encode(infor))
            rep=ClientSocket.recv(1024).decode('utf-8')
            ClientSocket.send(str.encode('OK'))
            ClientSocket.close()
            break
        except socket.error as e:
            print('Server Error')
            return

    if rep != 'None':
        print(rep)
        return True, rep
    else:
        return False, rep


def Request_Regis(ClientSocket, infor):
    infor.insert(0, 'REGIS')
    infor=','.join(infor)
    rep=''
    while True:
        try:
            ClientSocket.send(str.encode(infor))
            rep=ClientSocket.recv(1024).decode('utf-8')
            ClientSocket.send(str.encode('OK'))
            ClientSocket.close()
            break
        except socket.error as e:
            print('Server Error')
            return False, rep
    if rep != 'None':
        return True, rep
    else:
        return False, rep

def Request_SaveResult(ClientSocket, infor):
    infor.insert(0, 'SAVE')
    infor=','.join(infor)
    rep=''
    while True:
        try:
            ClientSocket.send(str.encode(infor))
            rep=ClientSocket.recv(1024).decode('utf-8')
            ClientSocket.send(str.encode('OK'))
            ClientSocket.close()
            break
        except socket.error as e:
            print('Server Error')
            return
    if rep != 'None':
        return True
    else:
        return False

def Request_GetData(ClientSocket):
    infor='GET_DATA'
    rep=''

    ClientSocket.send(str.encode(infor))
    connbuf = Buffer(ClientSocket)
    while True:
        hash_type = connbuf.get_utf8()
        if not hash_type:
            break
        file_name = connbuf.get_utf8()
        if not file_name:
            break
        file_name = os.path.join('Gamedata',file_name)
        print('file name: ', file_name)

        file_size = int(connbuf.get_utf8())
        print('file size: ', file_size )

        with open(file_name, 'wb') as f:
            remaining = file_size
            while remaining:
                chunk_size = 4096 if remaining >= 4096 else remaining
                chunk = connbuf.get_bytes(chunk_size)
                if not chunk: break
                f.write(chunk)
                remaining -= len(chunk)
            if remaining:
                print('File incomplete.  Missing',remaining,'bytes.')
            else:
                print('File received successfully.')
    
    print('Connection closed.')
    ClientSocket.close()



            
