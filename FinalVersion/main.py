from tests import simulation
import os
from multiprocessing import Process


def runSim(index,cur_dir,errorChanceArray,randomness,numOfSimulations):
    counter=0
    result=0
    debug=True
    for j in range(0,2,1):
        counter=0
        rate=-1
        path=cur_dir+"\\projectSimulation\\simulation" + str(index+j) +".txt"
        f=open(path,"a")
        f.write("Simulation with error chance: " +str(errorChanceArray[index+j])+"\n")
        f.close()
        for i in range(0,numOfSimulations):
            result=simulation(debug, path,randomness,errorChanceArray[index+j])
            counter+=result[0]
            if (result[1]!=0):
                rate=result[1]
        f=open(path,"a")
        f.write("Simulation results:\n")
        f.write("Success rate: " +str(counter/numOfSimulations)+"\n")
        f.write("Rate: " + str(rate)+"\n")
        f.close()

counter=0
rate=0
numOfSimulations=20

errorChanceArrayTmp = range(1, 100, 10)
errorChanceArray = [i/(10**6) for i in errorChanceArrayTmp]

debug = True
cur_dir = "C:\\Users\\voloshr\\Dekstop"
curR=open("C:\\Users\\voloshr\\Dekstop\\R.txt","r")

myPath = os.getcwd()
os.chdir(cur_dir)
directory = "projectSimulation"
if not os.path.exists(directory):
    os.makedirs(directory)

j = 0
randomness=curR.read()
processes=[]
for j in range(0,len(errorChanceArray),2):
    processes.append(Process(target=runSim,args=(j, cur_dir, errorChanceArray,randomness,numOfSimulations)))
if (__name__=="__main__"):
    for p in processes:
        p.start()
    for p in processes:
        p.join()