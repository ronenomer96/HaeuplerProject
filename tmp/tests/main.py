# -*- coding: utf-8 -*-
import Player
import reedsolo as rs 
import math
import random
import Channel


errorChance=0.1
seedSize=5000
hashSize=100
iterSize=20 #k
iterNum=1000 #n0
prngSeedSize=4*math.ceil(math.sqrt(errorChance)*iterNum)
#prngSeedSize = 10000
outerLoopNum=10000 #N

Alice=Player.Player("Alice",True,hashSize,seedSize)
Bob=Player.Player("Bob",False,hashSize,seedSize)
randomSeed=Alice.createShortPrngSeed(prngSeedSize)
Alice.createR(randomSeed,iterNum**2)

#transfer seed between both parties
numofsymbolstocorrect=math.ceil(len(randomSeed)*errorChance)
encdec = rs.RSCodec(numofsymbolstocorrect)
encodedSeed=encdec.encode(randomSeed)

prngSeedMsg=Channel.Channel(encodedSeed.decode("latin-1"),errorChance)

receivedSeed=encdec.decode(prngSeedMsg.encode("latin-1"))
Bob.createR(receivedSeed.decode("latin-1"),iterNum**2)

for i in range(0,1):
    aHashes=Alice.computeHashes()
    bHashes=Bob.computeHashes()
    aMsgs=[]
    bMsgs=[]
    for j in range (0,4):
        aMsgs.append(Channel.Channel(aHashes[j]))
        bMsgs.append(Channel.Channel(bHashes[j]))
    Alice.receiveHashes(bMsgs)
    Bob.receiveHashes(aMsgs)
    for j in range (0,iterSize):
        #Alice's part
        if (Alice.computeHashes()):
            msg=Alice.runTurn()
            Bob.receiveMsg(Channel.Channel(msg))
        else:
            Bob.receiveMsg(Channel.Channel(str(random.randint(0,1))))
        #Bob's part
        if (Bob.computeHashes()):
            msg=Bob.runTurn()
            Alice.receiveMsg(Channel.Channel(msg))
        else:
            Alice.receiveMsg(Channel.Channel(str(random.randint(0,1))))
    Alice.rewind()
    Bob.rewind()
       
        