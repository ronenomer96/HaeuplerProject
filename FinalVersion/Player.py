# -*- coding: utf-8 -*-
import math
import Hash_fun
import JumpingPointer as JP
import Converter
import random
import reedsolo as rs
import linearPRNG


class Player:
    def __init__(self,name,isStart,prngSeedLength,hashLength,protoLength,pi_0,errorChance,k,c):
        self.name = name

        self.isStart=isStart
        self.errorChance=errorChance
        self.currentProtoStage=1 #0 - for normal msgs, 1 - for hashes,2 - for seed
        self.prngSeedLength=prngSeedLength #to create R
        self.prngSeedLength -= prngSeedLength%8

        if (self.prngSeedLength==0):
            self.prngSeedLength=8

        self.ECCnum=-1

        tmp=prngSeedLength/8
        if (tmp > 255):
            self.ECCnum = math.ceil(Converter.cal_Symbol_error(errorChance) * 255) * 2 + 2
        else:
            self.ECCnum = 2 * Converter.calc_r(tmp, errorChance)

        self.hashSeedLength = 100*c*math.ceil(protoLength+math.log(protoLength,2))
        self.pi_0=pi_0
        self.prngSeed=""
        self.receivedHashes = []
        self.pi_0_loop_counter = 0
        self.k = k

        self.gap=0
        self.gap_error=0
        self.R=""
        self.originalR=""
        self.hashLength=hashLength
        self.protoLength=protoLength
        self.mp1 = -1
        self.mp2 = -1
        self.vote_mp1 = 0
        self.vote_mp2 = 0
        self.transcript = ""
        self.logGap = -1
        self.Hgap = ""
        self.Ht = ""
        self.Hmp1 = ""
        self.Hmp2 = ""
        self.m = -1
        return

    def getMsg(self):
        if (self.currentProtoStage==0): #run normal msg
            self.pi_0_loop_counter+=1
            msg=""
            if (self.IsIterValid()):
                msg = self.pi_0.getMsg()
                self.transcript += msg
            else:
                msg = str(random.randint(0, 1))
            if ((self.pi_0_loop_counter==self.k-1) and self.name=="Bob"):
                self.currentProtoStage=1
                self.pi_0_loop_counter=0
                if(self.IsIterValid()):
                    self.resetRewindParams()
                self.checkRewind()
            return msg

        elif (self.currentProtoStage==1): #run hashes
            self.calcHashes()
            if (self.name=="Bob"):
                self.checkHashes()
                self.currentProtoStage=0
            return self.getHashes() #is list

        else: #run seed
            if (self.isStart): #meaning this player needs to create the seed and return it
                self.prngSeed=self.getSeed()
                self.currentProtoStage=1
                self.createR()
                return self.encodeSeed()
            return -1
        return

    def putMsg(self,msg):
        if (self.currentProtoStage==0): #read normal msg
            if (self.IsIterValid()):
                self.pi_0.putMsg(msg)
                self.transcript += msg

            if ((self.pi_0_loop_counter ==self.k-1) and self.name=="Alice"):
                self.currentProtoStage=1
                self.pi_0_loop_counter=0
                if(self.IsIterValid()):
                    self.resetRewindParams()
                self.checkRewind()



        elif (self.currentProtoStage==1): #read hashes
            self.receiveHashes(msg)
            if (self.name=="Alice"):
                self.checkHashes()
                self.currentProtoStage=0

        else: #read seed
            self.decodeSeed(msg)
            self.createR()
            self.currentProtoStage=1
        return

    def getSeed(self):
        shortRandom = random.randint(0, 2 ** self.prngSeedLength - 1)
        finalPrngSeed = bin(shortRandom)[2:]
        if (len(finalPrngSeed) < self.prngSeedLength):
            finalPrngSeed = finalPrngSeed.zfill(self.prngSeedLength)
        return finalPrngSeed

    def encodeSeed(self):
        A_HexSeed = Converter.RSEncodeConv(self.prngSeed)
        rsObj = rs.RSCodec(self.ECCnum)
        A_RsSeed = rsObj.encode(A_HexSeed)
        return Converter.RSDecodeConv(A_RsSeed, self.prngSeedLength + 8 * self.ECCnum)

    def decodeSeed(self,seedAsBin):
        B_RsSeed = Converter.RSEncodeConv(seedAsBin)
        rsObj = rs.RSCodec(self.ECCnum)
        B_HexSeed = rsObj.decode(B_RsSeed)
        B_Seed = Converter.RSDecodeConv(B_HexSeed, self.prngSeedLength)
        self.prngSeed=B_Seed
        return

    def createR(self):
        neededLength=self.protoLength**2
        if (neededLength > 10 ** 8):
            self.R = linearPRNG.linearPRNG(self.prngSeed, 10 ** 8)  # because we cannot compute higher values
        else:
            self.R = linearPRNG.linearPRNG(self.prngSeed, neededLength)
        self.originalR=self.R
        return
    def setR(self,R):
        self.R=R
        self.originalR=R
        return
    def strToBin(self, num):
        return bin(num)[2:]

    '''
    def runStep(self):
        currentStep=self.jp.get_cur_decision(self.currentVertexNum)
        self.currentVertexNum=self.currentVertexNum*2+currentStep
        self.transcript+=str(currentStep) 
        return str(currentStep)

    def receiveStep(self,step):
        self.transcript+=step
        self.currentVertexNum=self.currentVertexNum*2+int(step)
        return

    def appendT(self,msg):
        self.transcript=self.transcript+msg
        return
    '''

    def getTrans(self):
        return self.transcript

    def resetRewindParams(self):
        self.gap=0
        self.vote_mp1=0
        self.vote_mp2=0
        return

    def calcHashes(self):
        self.gap=self.gap+1
        self.logGap=math.floor(math.log(self.gap, 2))
        self.m = Converter.calc_m(self.transcript, self.logGap)
        self.mp1 = int(self.m * (2 ** self.logGap))
        self.mp2 = int(max((self.m - 1) * (2** self.logGap), 0))

        if (self.mp1%2!=0):
            self.mp1-=1
        if (self.mp2%2!=0):
            self.mp2-=1

        if len(self.R) < self.hashSeedLength:
            self.R=self.originalR
        currentSeed=self.R[0:self.hashSeedLength]
        self.R=self.R[self.hashSeedLength+1:]
        #tmp=str(self.gap)

        gapStr = self.strToBin(self.gap)
        gapStrLen = self.strToBin(len(gapStr))
        self.Hgap=Hash_fun.hash_fun(currentSeed,gapStr+gapStrLen,self.hashLength)
        self.Ht=Hash_fun.hash_fun(currentSeed,self.transcript+bin(len(self.transcript))[2:],self.hashLength)
        self.Hmp1=Hash_fun.hash_fun(currentSeed,self.transcript[0:self.mp1]+bin(len(self.transcript[0:self.mp1]))[2:],self.hashLength)
        self.Hmp2=Hash_fun.hash_fun(currentSeed,self.transcript[0:self.mp2]+bin(len(self.transcript[0:self.mp2]))[2:],self.hashLength)
        return

    def getHashes(self):
        return [self.Hgap,self.Ht,self.Hmp1,self.Hmp2]

    def receiveHashes(self,receivedHashes):
        self.receivedHashes=receivedHashes
        return

    def checkHashes(self):
        if self.Hgap != self.receivedHashes[0]:
            self.gap_error=self.gap_error+1
        else:
            if (self.Hmp1==self.receivedHashes[2] or self.Hmp1==self.receivedHashes[3]):
                self.vote_mp1=self.vote_mp1+1
            if (self.Hmp2==self.receivedHashes[2] or self.Hmp2==self.receivedHashes[3]):
                self.vote_mp2=self.vote_mp2+1
        return

    def compareHashes(self):
        if self.receivedHashes != [self.Hgap,self.Ht,self.Hmp1,self.Hmp2]:
            return False
        else:
            return True

    def IsIterValid(self):
        if (self.compareHashes() and self.gap==1):
            return True
        else:
            return False

    def checkRewind(self):
        if 2*self.gap_error >= self.gap:
            self.gap_error=0
            self.gap=0
        else:
            if self.gap == 2**self.logGap:
                if self.vote_mp1 >= 0.4*(2**self.logGap):
                    self.gap=0
                    self.transcript=self.transcript[0:self.mp1]
                else:
                    if self.vote_mp2 >= 0.4*(2**self.logGap):
                        self.gap=0
                        self.transcript=self.transcript[0:self.mp2]
                self.vote_mp1=0
                self.vote_mp2=0
                self.pi_0.ResetVertexNum()

                for i in range(0,len(self.transcript)):
                    self.pi_0.putMsg(self.transcript[i])
        return 

    def getR(self):
        return self.R