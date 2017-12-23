"""
Input 
 seed- starting seed (X0)
 desiredLength- length of the desired output
"""
import numpy as np
import math
import datetime
import random
m=np.int((2**31)-1)
a=np.int(48271)
def linearPRNG(seed,desiredLength):
    newString=seed
    listOfStrings=[newString[start:start+32] for start in range(0,len(newString),32)]
    numberOfX=len(listOfStrings)
    aLength=math.ceil(desiredLength/(numberOfX*32))
    prev=np.int(1)
    aVec=np.array([])
    for i in range(0,aLength,1):
        prev=(a*prev)%m
        aVec=np.append(aVec,prev)
    aVec=np.asmatrix(aVec).transpose()
    xVec=np.array([int(curStr,2) for curStr in listOfStrings])
    xVec=np.asmatrix(xVec)
    sol=np.squeeze(np.asarray(((aVec.dot(xVec))%m).flatten().transpose()))
    strlist=[]
    for curVal in sol:
        strlist.append(np.binary_repr(int(curVal),32))
    return ''.join(strlist)


x=random.randint(0,2**1000-1)
y=bin(x)[2:]    
print(datetime.datetime.now())
z=linearPRNG(y,10**6)
print(datetime.datetime.now())
print(len(z))'   