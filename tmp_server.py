import socket
from JumpingPointer import JumpingPointer

host = ''        # Symbolic name meaning all available interfaces
port = 12345     # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
k = 2
curNodeNum = 0
curString = ""
A = JumpingPointer(conn)
i = 10
for j in range(0 , k):
    print("omer", i)
    tmp = A.get_cur_decision(curNodeNum)
    print("omer", i+1, tmp, type(tmp))
    A.send_message(tmp)
    print("omer", i+2)
    curString += str(tmp)
    print("omer", i+3)
    curNodeNum = curNodeNum*2 + (tmp+1)
    print("omer", i+4, curNodeNum)
    tmp = A.rec_message()
    print("omer", i+5, tmp, type(tmp))
    curString += str(int.from_bytes(tmp, byteorder = 'little'))
    print("omer", i+6)
    curNodeNum = curNodeNum*2 + (int.from_bytes(tmp, byteorder = 'little')+1)
    print("omer", i+7, curNodeNum)
print(curString)

s.close()
