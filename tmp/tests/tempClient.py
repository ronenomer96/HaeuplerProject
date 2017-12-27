import socket
from JumpingPointer import JumpingPointer
host="172.18.30.9"
port=12345
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host, port))
k=2
curNodeNum=0
curString=""
A=JumpingPointer(s)
for i in range(0,k):
    tmp=A.rec_message()
    curString+=str(int.from_bytes(tmp,byteorder='little'))
    curNodeNum=curNodeNum*2+(int.from_bytes(tmp,byteorder='little')+1)
    tmp=A.get_cur_decision(curNodeNum)
    A.send_message(tmp)
    curString+=str(tmp)
    curNodeNum=curNodeNum*2+(tmp+1)
print(curString)
s.close()
