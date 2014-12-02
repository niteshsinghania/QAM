# -*- coding: utf-8 -*-

# Imports
import apriorialg as ap
import Data
import numpy as np


maxSupport = 0.24
minSupport = 0.24
minConfidence = 0.8
K = 17
R = 10

# Read the data
columnNames = ['W','AB','H','2B','3B','HR','BB','SO','SB','RA','HA','HRA','BBA','SOA','E']
tableName = ['Teams']

data = Data.Data(columnNames,tableName[0])
columnIntervals = data.createColumnIntervals(minSupport,K)

theData = data.loadData()

L, sup_data = ap.apriori(theData, columnIntervals,columnNames, minSupport, maxSupport, R)


rules = ap.generateRules(L, sup_data, minConfidence)

stats = []
for rule in rules:
    stats.append(rule[2])
statsMean =  np.mean(stats,axis = 0)
statsStd = np.std(stats, axis = 0)


#print rank
for rule in rules:
    rank = 0
    for index in range(len(statsMean)):
        if ((rule[2][index] - statsMean[index]) > 0):
            rank += ((rule[2][index] - statsMean[index])/ statsStd[index])
        else:
            rank += ((statsMean[index] - rule[2][index])/ statsStd[index])
        rule[2].append(rank)
sortedRules = sorted(rules, key = lambda x: x[2][4])

sortedRulesW = []

for rule in sortedRules:
    x = rule[0]
    y = rule[1]
    foundInx = False
    foundIny = False
    for interval in x:
        if (interval.name == 'W'):
            foundInx = True
        for interval in y:
            if (interval.name == 'W'):
                foundIny = True

    if(foundInx == True or foundIny == True ):
        sortedRulesW.append(rule)


for rule in sortedRulesW[0:10]:
    rule_str = ""
    x = rule[0]
    y = rule[1]


    for interval in x:
        rule_str += interval.hStr() + ", "
    rule_str += " --> "
    for interval in y:
        rule_str += interval.hStr() + ", "

    rank = rank/len(statsMean)
    rule_str += "\n"
    rule_str += " Confidence: " + str(rule[2][0])
    rule_str += "\n"
    rule_str += " Interest: " + str(rule[2][1])
    rule_str += "\n"
    rule_str += " PS: " + str(rule[2][2])
    rule_str += "\n"
    rule_str += " Conv: " + str(rule[2][3])
    rule_str += "\n"
    rule_str += " Rank: " + str(rank)

    print(rule_str)
