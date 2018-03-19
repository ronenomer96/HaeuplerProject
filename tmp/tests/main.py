# -*- coding: utf-8 -*-
import Player
import reedsolo as rs 
import math
import random
import Channel

#add max length to protocol to stop

errorChance=0.001
seedSize=10
iterSize=20 #k
protoLength=1000#n0
prngSeedSize=4*math.ceil(math.sqrt(errorChance)*protoLength)
hashLength=100
outerLoopNum=10000 #N

Alice=Player.Player("Alice",True,seedSize)
Bob=Player.Player("Bob",False,seedSize)
randomSeed=Alice.createShortPrngSeed(prngSeedSize)
Alice.createR(randomSeed,protoLength**2,hashLength,protoLength)
#transfer seed between both parties
numofsymbolstocorrect=math.ceil(len(randomSeed)*errorChance)
encdec = rs.RSCodec(numofsymbolstocorrect)
encodedSeed=encdec.encode(randomSeed)

prngSeedMsg=Channel.Channel(encodedSeed.decode("latin-1"),errorChance)

receivedSeed=encdec.decode(prngSeedMsg.encode("latin-1"))
Bob.createR(receivedSeed.decode("latin-1"),protoLength**2,hashLength,protoLength)

for i in range(0,1):
    aHashes=Alice.computeHashes()
    bHashes=Bob.computeHashes()
    aMsgs=[]
    bMsgs=[]
    for j in range (0,4):
        aMsgs.append(Channel.Channel(aHashes[j],errorChance))
        bMsgs.append(Channel.Channel(bHashes[j],errorChance))
    Alice.receiveHashes(bMsgs)
    Bob.receiveHashes(aMsgs)
    for j in range (0,iterSize):
        #Alice's part
        if (Alice.compareHashes()):
            msg=Alice.runTurn()
            Bob.receiveMsg(Channel.Channel(msg,errorChance))
        else:
            Bob.receiveMsg(Channel.Channel(str(random.randint(0,1)),errorChance))
        #Bob's part
        if (Bob.compareHashes()):
            msg=Bob.runTurn()
            Alice.receiveMsg(Channel.Channel(msg,errorChance))
        else:
            Alice.receiveMsg(Channel.Channel(str(random.randint(0,1)),errorChance))
    Alice.rewind()
    Bob.rewind()
print(Alice.prot.transcript)
print(Bob.prot.transcript)
print(Alice.prot.transcript==Bob.prot.transcript)       
        