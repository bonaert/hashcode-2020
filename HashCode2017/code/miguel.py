#usr/bin/env/python
#coding: utf8

__author__ = "Miguel"
__date__ = "23/02/2017"

import sys

filename = "../Data/{}.in".format(sys.argv[1])

with open(filename) as dt:
    info = dt.readline()
    sizes = dt.readline()
    info = info.split()
    numVid = int(info[0])
    numEnd = int(info[1])
    reqDes = int(info[2])
    numCac = int(info[3])
    cacSize = int(info[4])
    endPoints = [[] for i in range(numEnd)]
    cacConnect = [[] for i in range(numCac)]
    cacExclude = [[] for i in range(numCac)]
    for i in range(numEnd):
        lat, num = dt.readline().split()
        num = int(num)
        for j in range(num):
            cac, lat = dt.readline().split()
            endPoints[i].append(int(cac))
            
    for i in range(len(endPoints)):
        for j in range(len(endPoints[i])):
            cacConnect[endPoints[i][j]].append(i)
    
    restData = dt.readlines()
    for line in restData:
        line = line.split()
        vidNum = int(line[0])
        endNum = int(line[1])
        for caci in endPoints[endNum]:
            if vidNum not in cacExclude[caci]:
                cacExclude[caci].append(vidNum)
    
    
print(endPoints)
print(cacConnect)
print(cacExclude)

sizes = sizes.split()
vidSizes = {}
for i in range(len(sizes)):
    vidSizes[i] = int(sizes[i])
    sizes[i] = int(sizes[i])

outfile = "{}.out".format(sys.argv[1])

test = [[] for i in range(numCac)]
testGood = [[] for i in range(numCac)]
cache = 0

for i in range(len(sizes)):
    if sum(test[cache] + [sizes[i]]) < cacSize:
        if i in cacExclude[cache]:
            test[cache].append(sizes[i])
            testGood[cache].append(i)
        else:
            fin = False
            for k in range(len(cacExclude)):
                if i in cacExclude[k] and not fin and sum(test[k] + [sizes[i]]) < cacSize:
                    test[k].append(sizes[i])
                    testGood[k].append(i)
                    fin = True
                    
    else:
        if cache < numCac-1:
            cache += 1
            if sum(test[cache] + [sizes[i]]) < cacSize:
                test[cache].append(sizes[i])
                testGood[cache].append(i)
        else:
            pass
             

numFill = 0
for n in testGood:
    if len(n) > 0:
        numFill +=1

with open(outfile, "w") as ot:
    ot.write("{}\n".format(numFill))
    for i in range(len(test)):
        testGood[i] = [str(n) for n in testGood[i]]
        if len(testGood[i]) > 0:
            ot.write(str(i)+ " " + " ".join(testGood[i])+"\n")
        
        
        
        
    

