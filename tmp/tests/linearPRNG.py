"""
Input 
 seed- starting seed (X0)
 desiredLength- length of the desired output
"""
import numpy as np
import random
c=0
m=np.int((2**31)-1)
a=np.int(48271)
def linearPRNG(seed,desiredLength):
    newString=seed
    listOfStrings=[newString[start:start+32] for start in range(0,len(newString),32)]
    listOfInts=[]
    for curStr in listOfStrings:
        listOfInts.append(int(curStr,2)) 
    while (len(newString) < desiredLength):
       tmpList=[]
       for curVar in listOfInts:
           tmp=((curVar*a)%m)
           newString+=np.binary_repr(tmp,32)
           tmpList.append(tmp)
       listOfInts+=tmpList
    return newString


x=random.randint(0,2**100-1)
y=bin(x)[2:]
z=linearPRNG(y,1000000)
print(z)
print(len(z))    