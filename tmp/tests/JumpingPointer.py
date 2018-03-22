import random
## change later to work without a socket ## 
class JumpingPointer:
    history={}
    def __init__(self):
        self.history={}
        return
    def get_cur_decision(self, vertex_num):
        if vertex_num in self.history.keys():
            return self.history[vertex_num]
        else:
            cur_choice = random.randint(0, 1)
            self.history[vertex_num] = cur_choice
            return cur_choice
    