import random
import socket

class JumpingPointer:
    history = {}
    our_soc = 0
    def __init__(self, out_soc):
        self.our_soc = out_soc
        return
    def get_cur_decision(self, vertex_num):
        if vertex_num in self.history.keys():
            return self.history[vertex_num]
        else:
            cur_choice = random.randint(0, 1)
            self.history[vertex_num] = cur_choice
            return cur_choice
    def send_message(self, vertex_num):
        self.out_soc.sendall(history[vertex_num])
        return
    def rec_massaged(self):
        return self.our_soc.recv(1024)


host = ''        # Symbolic name meaning all available interfaces
port = 12345     # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
while True:
    data = conn.recv(4)
    print (data)
    if not data:
        break
    conn.sendall(data)
conn.close()


A = JumpingPointer(s)
A.get_cur_decision(1)
A.get_cur_decision(2)
A.get_cur_decision(3)
A.get_cur_decision(4)
A.get_cur_decision(5)
print (A.history)
A.get_cur_decision(5)
print (A.history)

