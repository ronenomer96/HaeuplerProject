'''
import linearPRNG
import math
import random
curRandom=random.randint(0,2**(10**6))
curRandom=bin(curRandom)[2:]
if (len(curRandom)<10**6):
    curRandom.zfill(10**6)
fullRandomness=linearPRNG.linearPRNG(curRandom,10**9)

f=open("C:\\Users\\voloshr\\Dekstop\\R.txt","w+")
f.write(fullRandomness)
f.close()



errorChanceArray = range(1, 1000, 100)
errorChanceArrayNew = [i/(10**7) for i in errorChanceArray]
print(errorChanceArrayNew)

'''
errorChanceArrayTmp = range(1, 1000, 100)
errorChanceArray = [i/(10**7) for i in errorChanceArrayTmp]
for i in range(0,2,1):
    print(i)