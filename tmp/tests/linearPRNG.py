"""
Input 
 seed- starting seed (X0)
 desiredLength- length of the desired output
"""
import random
c=0
m=(2**31)-1
a=48271
def linearPRNG(seed,desiredLength):
    newString=seed
    while (len(newString)<desiredLength):
        listOfStrings=[newString[start:start+32] for start in range(0, len(newString), 32)]
        for curStr in listOfStrings:
            newString+=bin((int(curStr,2)*a)%m)[2:]
    return newString


x=random.randint(0,2**100-1)
y=bin(x)[2:]
z=linearPRNG(y,1000000)
print(z)
print(len(z))    