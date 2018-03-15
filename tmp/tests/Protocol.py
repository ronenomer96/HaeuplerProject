# -*- coding: utf-8 -*-
import math
import Hash_fun
import JumpingPointer as JP

class Protocol:
    seedLength=-1 # paramater (change in simulations)
    hashLength=-1 # parameter (change in simulations)  
    
    
    mp1=-1
    mp2=-1
    vote_mp1=0
    vote_mp2=0
    gap=0
    gap_error=0
    transcript=""
    originalR=""
    R=""
    
    l=-1
    Hgap=""
    Ht=""
    Hmp1=""
    Hmp2=""
    receivedHashes=[]
    
    jp= JP.JumpingPointer()
    currentVertexNum=-1
    
    def __init__(self,R,seedLength,hashLength,vertexNum):
        self.gap=0
        self.gap_error=0
        self.R=R
        self.originalR=R
        self.seedLength=seedLength
        self.hashLength=hashLength
        self.currentVertexNum=vertexNum;
        return
    
    
    def runStep(self):
        currentStep=self.jp.get_cur_decision(self.currentVertexNum)
        self.currentVertexNum=self.currentVertexNum*2+currentStep
        self.transcript+=currentStep
        return currentStep
    def receiveStep(self,step):
        self.transcript+=step
        self.currentVertexNum=self.currentVertexNum*2+step
        return 
    
    
    def appendT(self,msg):
        self.transcript=self.transcript+msg
        return
    def resetRewindParams(self):
        self.gap=0
        self.vote_mp1=0
        self.vote_mp2=0
        return
    def getHashes(self):
        self.gap=self.gap+1
        self.l=math.ceil(math.log(self.gap,2))
        self.mp1=math.floor(len(self.transcript)/math.pow(2,self.l))*math.pow(2,self.l)
        self.mp2=max((math.floor(len(self.transcript)/math.pow(2,self.l))-1)*math.pow(2,self.l),0)
        if len(self.R) < self.seedLength:
            self.R=self.originalR
        currentSeed=self.R[0:self.seedLength]
        self.R=self.R[self.seedLength+1:]
        tmp=str(self.gap)
        self.Hgap=Hash_fun.hash_fun(currentSeed,tmp,self.hashLength)
        self.Ht=Hash_fun.hash_fun(currentSeed,self.transcript,self.hashLength)
        self.Hmp1=Hash_fun.hash_fun(currentSeed,self.transcript[0:self.mp1],self.hashLength)
        self.Hmp2=Hash_fun.hash_fun(currentSeed,self.transcript[0:self.mp2],self.hashLength)
        return [self.Hgap,self.Ht,self.Hmp1,self.Hmp2]
    def checkHashes(self,receivedHashes):
        self.receivedHashes=receivedHashes
        if self.Hgap != receivedHashes[0]:
            self.gap_error=self.gap_error+1
        else:
            if (self.Hmp1==receivedHashes[2] or self.Hmp1==receivedHashes[3]):
                self.vote_mp1=self.vote_mp1+1
            if (self.Hmp2==receivedHashes[2] or self.Hmp2==receivedHashes[3]):
                self.vote_mp2=self.vote_mp2+1
        return
    def compareHashes(self,receivedHashes):
        if self.receivedHashes!= [self.Hgap,self.Ht,self.Hmp1,self.Hmp2]:
            return False
        else:
            return True
    def checkRewind(self):
        if 2*self.gap_err >= self.gap:
            self.gap_err=0
            self.gap=0
        else:
            if self.gap==2*self.l:
                if self.vote_mp1 >=0.4*math.pow(2,self.l):
                    self.gap=0
                    self.transcript=self.transcript[0:self.mp1]
                else:
                    if self.vote_mp2 >= 0.4*math.pow(2,self.l):
                        self.gap=0
                        self.transcript=self.transcript[0:self.mp2]
            self.vote_mp1=0
            self.vote_mp2=0
            self.currentVertexNum=0
            for i in range(0,len(self.transcript)):
                if self.transcipt[i]=="1":
                    self.currentVertexNum=self.currentVertexNum*2+1
                else:
                    self.currentVertexNum=self.currentVertexNum*2
        return 

    