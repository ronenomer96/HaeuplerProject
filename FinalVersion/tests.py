from Player import Player
from Channel import Channel
import JumpingPointer as JP
import math
import os
import datetime
import Converter

PREFIX = """
-----------------------------------------------------------------------------------
n0 is:                                    {n0}
error chance is:                          {errorChance}
c is:                                     {c}
k is:                                     {k}
N is:                                     {N}
cc of prot:                               {cc_of_prot}
Success probability for a block:          {succ_prob}
-----------------------------------------------------------------------------------
"""



def simulation(debug, path,randomness,errChance):
    #define variables
    c=2
    errorChance= errChance
    hashLength=c #O(1)
    k=math.ceil(0.5*math.sqrt(c/errorChance))
    n0=10**3 #protoLength
    prngSeedLength=math.ceil(math.sqrt(n0))
    N=math.ceil((n0/k)+65*n0*errorChance) #RAN was 65
    numOfErrors=0
    cc_of_prot = str(N*(2*k +8*c))
    succ_prob = str((1-errorChance)**(2*k +8*c))
    flag = False
    ccOfProto = 0

    if(debug):
        code = ""
        code+="Simulation started at time: " +str(datetime.datetime.now()) +"\n"
        #to write the code
        keys = {
            "n0":n0 ,
            "errorChance":errorChance ,
            "c":c ,
            "k":k ,
            "N":N ,
            "cc_of_prot":cc_of_prot ,
            "succ_prob":succ_prob
        }
        code += PREFIX.format(**keys)

    #create the players
    Alice=Player("Alice",True,prngSeedLength,hashLength,n0,JP.JumpingPointer(),errorChance,k,c)
    Bob = Player("Bob",False,prngSeedLength,hashLength,n0,JP.JumpingPointer(),errorChance,k,c)
    Alice.setR(randomness)
    Bob.setR(randomness)

    if (Alice.getR()!=Bob.getR()):
        print("R is inconsistent")
        return 0
    if (debug):
        code+="R is consisntent\n"

    for i in range(0,N*k):
       # print(i)
        msg=Alice.getMsg()
        tmp = Channel(msg, errorChance)
        msgChannel = tmp[0]
        numOfErrors += tmp[1]
        if (type(msg)is str):
            ccOfProto+=len(msg)
            if (debug):
                if (msg!=msgChannel):
                    code += "Original msg (regular msg): " + msg +", Msg after channel: " + msgChannel + ", Block number is: "+ str(int(i/k))+ ", Iteration number is: "+str(i%k)+"\n"
        else:
            if (debug):
                if (msg!=msgChannel):
                    code += "Hash msg: " + msg[0]+msg[1]+msg[2]+msg[3] + ", Hash after channel: " + msgChannel[0]+msgChannel[1]+msgChannel[2]+msgChannel[3] +", Block number is: "+ str(int(i/k))+"\n"
            ccOfProto+=hashLength*4

        Bob.putMsg(msgChannel)

        msg=Bob.getMsg()
        tmp = Channel(msg, errorChance)
        msgChannel = tmp[0]
        numOfErrors += tmp[1]
        if (type(msg) is str):
            ccOfProto += len(msg)
            if (debug):
                if (msg != msgChannel):
                    code += "Original msg (regular msg): " + msg + ", Msg after channel: " + msgChannel + ", Block number is: " + str(int(i / k)) + ", Iteration number is: " + str(i % k) + "\n"
        else:
            if (debug):
                if (msg != msgChannel):
                    code += "Hash msg: " + msg[0] + msg[1] + msg[2] + msg[3] + ", Hash after channel: " + msgChannel[0] + msgChannel[1] + msgChannel[2] + msgChannel[3] + ", Block number is: " + str(
                        int(i / k)) + "\n"
            ccOfProto += hashLength * 4

        Alice.putMsg(msgChannel)
    if (debug):
        code+="-----------------------------------------------------------------------------------\n"
        code+="alice trans == bob trans: " + str(Alice.getTrans()[0:n0] == Bob.getTrans()[0:n0])+"\n"
        code+="num of errors: " + str(numOfErrors)+"\n"
        code+="num of errors/n: " + str(numOfErrors / ccOfProto)+"\n"
    if(Alice.getTrans()[:n0]==Bob.getTrans()[:n0] and len(Alice.getTrans()[:n0])==n0):
        if (debug):
            code+="Success \n"
            code += "Simulation ended at time: " + str(datetime.datetime.now()) + "\n"

            code += "-----------------------------------------------------------------------------------\n"
            f = open(path, "a")
            f.write(code + "\nSimulation Ended\n\n\n")
            f.close()
        return [1,n0/ccOfProto,n0]
    else:
        if (debug):
            code+="Failed \n"
            code+="Alice's transcript length: " + str(len(Alice.getTrans())+"\n")
            code+="Bob's transcript length: " + str(len(Bob.getTrans())+"\n")
            code += "Simulation ended at time: " + str(datetime.datetime.now()) + "\n"
            code += "-----------------------------------------------------------------------------------\n"
            f = open(path, "a")
            f.write(code + "\nSimulation Ended\n\n\n")
            f.close()
        return [0,0]

