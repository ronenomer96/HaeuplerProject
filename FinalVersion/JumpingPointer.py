import random
class JumpingPointer:
    def __init__(self):
        self.history={}
        self.currentVertexNum=1
        return

    def getMsg(self):
        valToReturn=-1
        if self.currentVertexNum in self.history.keys():
            valToReturn= self.history[self.currentVertexNum]
        else:
            valToReturn= int(random.randint(0, 1))
            self.history[self.currentVertexNum] = valToReturn
        self.currentVertexNum = self.currentVertexNum * 2 + valToReturn
        return str(valToReturn)

    def putMsg(self,msg):
        #self.history[self.currentVertexNum] =int(msg)
        self.currentVertexNum =self.currentVertexNum*2 + int(msg)
        return

    def ResetVertexNum(self):
        self.currentVertexNum=1
        return




'''
    def getMsg(self):
        valToReturn = -1
        if (self.currentVertexNum < 2**50):
            valToReturn= 0
        else:
            valToReturn= 1
        self.currentVertexNum*=2
        self.currentVertexNum+=valToReturn
        return str(valToReturn)

    def putMsg(self, msg):
        # self.history[self.currentVertexNum] =int(msg)
        self.currentVertexNum = self.currentVertexNum * 2 + int(msg)
        return
   '''
