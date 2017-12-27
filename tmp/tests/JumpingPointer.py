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
    def send_message(self, byte_to_send):
        self.our_soc.sendall(bytes([byte_to_send]))
        return
    def rec_message(self):
        return self.our_soc.recv(1)
