
# -*- coding: utf-8 -*-
import codecs
import numpy as np   # gets some useful functions such as special arrays, dot-product, etc.
import numpy.linalg as npla # gets some specialized linear algebra functions such as vector length (normalization), etc.
import loadFile as lf
import random
import scipy
import math
from sklearn.metrics import *
from matplotlib.mlab import PCA     # gets the PCA class
from matplotlib import pyplot as plt

def load_dataset():

    labelsMatrix = []
    columns = [6,8,9,14,15,16,17,18,19,20,21,22,26,27,28,33,34,35,36,37]
    thedata = lf.load_data_from_file("Teams.csv",columns)



    def createLables(labelsArray, label):
        newLables = []
            
        for j in range(len(labelsArray)):
            labelToAdd = label
            labelToAdd += `labelsArray[j]`
            newLables.append(labelToAdd)
        return newLables


    def findClosestCentroid (centroid, point):
        
        closest = None
        closestDistance = 99999999999
            
        for cent in range (0, len(centroid)):
                
            total = 0
            
            total += (point[0]-centroid[cent][0])**2
            total += (point[1]-centroid[cent][1])**2
            
            distance = math.sqrt(total)
            
            if distance < closestDistance:
                closest = cent
                closestDistance = distance
        return closest

    def findClassLimits (labelsArray, xAxis, kvalue):
        max = 0
        min = 0
        groupRange = []
        minAndMax = []
        
        for i in range(kvalue):
            count = 0
            for j in range(len(labelsArray)):
                if(i == labelsArray[j]):
                    count+=1
                    groupRange.append(xAxis[j])
            min = np.min(groupRange)
            max = np.max(groupRange)
            minAndMax.append(min)
            minAndMax.append(max)
        minAndMax.sort()
        return minAndMax
    

    myArray = ['G','W','L','R','AB','H','2B','3B','HR','BB','SO','SB','RA','ER','ERA','HA','HRA','BBA','SOA','E']


    yAxis = thedata[2327:,1]
    xAxis = thedata[2327:,:]


    for index in range(1,len(thedata[0,:])):

        xAxis = thedata[2327:,index]
        minval = np.min(xAxis[np.nonzero(xAxis)])
        maxval = np.max(xAxis[np.nonzero(xAxis)])
        
        kvalue = maxval - minval
        
        kvalue = kvalue/2
        kvalue = int((kvalue)**0.5)

        if (kvalue > 2):
            kvalue = int(kvalue/2)
        
        if (kvalue < 2):
            kvalue = 2



        """
        myPCA = PCA(np.array(thedata))

        xAxis = myPCA.Y[:,0]

        yAxis = myPCA.Y[:,1]
        """



        # May wish to initialize k-value, iterations and centroids

        #max iterations
        iterations = 1000

        """
        Determine SSE values for clusters, and data
        """


        # initialize cluster centroid positions
        size = 120/kvalue
        pos = size
        oldPos = 0
        initRanSmpl = []
        initRanSmplValue = 0
        randSmpl = []
        #randSmpl = random.sample(xrange(len(xAxis)), kvalue)


        for value in range(kvalue):
            initRanSmpl = random.sample(xrange(oldPos,pos), kvalue)
            initRanSmplValue = sum(initRanSmpl)/len(initRanSmpl)
            randSmpl.append(initRanSmplValue)
            oldPos = pos
            pos = pos + size

        centroid = []
        oldCentroid = []

        for x in randSmpl:
            point = [xAxis[x],yAxis[x]]
            centroid.append(point)


        XArrayLables = [0]*len(xAxis)

        keepGoing = 1
        count = 0
        sumSEEArray = []

        for x in range(iterations ):
            sumSEEArray = []
            # Repeat steps of k-means until convergence or a fixed number of iterations is done
            if (keepGoing == 1):
                groups = [[] for i in range(kvalue)]
                for i in range(0, len(xAxis)):
                    point = [xAxis[i],yAxis[i]]
                    closestCentroid = findClosestCentroid(centroid, point)
                    groups[closestCentroid].append(point)
                    XArrayLables[i] = closestCentroid
                oldCentroid = centroid
                centroid = []
                for gI in range(len(groups)):
                    g=groups[gI]
                    sumX=0
                    sumY=0
                    total=0
                    sumSEE=0
                    overallScore=0
                    for z in g:
                        sumX = sumX+z[0]
                        sumY = sumY+z[1]
                    meansX=sumX/len(g)
                    meansY=sumY/len(g)
                    point = [meansX,meansY]
                    centroid.append(point)
                    total += (centroid[gI][0]-oldCentroid[gI][0])**2
                    total += (centroid[gI][1]-oldCentroid[gI][1])**2
                    distance = math.sqrt(total)
                    #SSE calculation
                    for z in g:
                        sumSEE += (point[0]-z[0])**2
                        sumSEE += (point[1]-z[1])**2
                    sumSEE = math.sqrt(sumSEE)
                    sumSEE = sumSEE/len(g)
                    sumSEEArray.append(sumSEE)
                if distance == 0.0:
                    count=count+1
                    if count == kvalue:
                        keepGoing = 0
                        #calculate overall score
                        overallScore = silhouette_score(thedata, np.array(XArrayLables) , metric='euclidean')
                        #print "SSE = ",sumSEEArray
                        #print "overall score = ", overallScore
                        #print "iterations = ",x


        """
        Visualize the relationship between known class labels, and cluster assignments
        """
        #plt.scatter(xAxis,yAxis,c=np.array(XArrayLables))
        #plt.plot(xAxis, yAxis)
        #plt.title(myArray[index])
        #plt.show()
        #print myArray[index]
        #minAndMax = findClassLimits (XArrayLables, yAxis,kvalue)
        #count = 0
        #for val in range(kvalue):
            #createLabel = myArray[index]
            #createLabel +=`val`
            #print createLabel
            #print minAndMax[count],' ',minAndMax[count+1]
            #print
            #count+=2
        toAppend = createLables( XArrayLables,myArray[index])
        labelsMatrix.append(toAppend)

    labelsMatrixTransposed = np.array(zip(*labelsMatrix))
    return labelsMatrixTransposed
