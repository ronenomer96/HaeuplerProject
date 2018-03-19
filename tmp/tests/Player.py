# -*- coding: utf-8 -*-
import Protocol
import random
import linearPRNG
class Player:
    name=""
    turn=False
    seedLength=-1
    prot=0
    def __init__(self,name,turn,seedLength):
        self.name=name
        self.turn=turn
        self.seedLength=seedLength
        return
    
    def createShortPrngSeed(self,prngSeedSize):
         if (self.name=="Alice"):
             shortRandom=random.randint(0,2**prngSeedSize-1)
             finalPrngSeed=bin(shortRandom)[2:]
             if (len(finalPrngSeed)<prngSeedSize):
                 finalPrngSeed=finalPrngSeed.zfill(prngSeedSize)
             return finalPrngSeed
         return -1
    
    def createR(self,prngSeed,neededLength,hashLength,protoLength):
        if (neededLength > 10**8):
            R=linearPRNG.linearPRNG(prngSeed,10**8) #because we cannot compute higher values
        else:
            R=linearPRNG.linearPRNG(prngSeed,neededLength)
        self.prot=Protocol.Protocol(R,1,hashLength,protoLength)
        return 
    def computeHashes(self):
        return self.prot.getHashes()
    def compareHashes(self):
        return self.prot.compareHashes()
    def receiveHashes(self,hashes):
        self.prot.checkHashes(hashes)
        return
    def rewind(self):
        self.prot.checkRewind()
        return 
    def runTurn(self):
        return self.prot.runStep()
    def receiveMsg(self,msg):
        self.prot.receiveStep(msg)
        return
       