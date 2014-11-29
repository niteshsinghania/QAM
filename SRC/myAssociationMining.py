# -*- coding: utf-8 -*-

# Imports
import apriorialg as ap
import Data

minSupport = 0.05
minConfidence = 0.001
k = 5

# Read the data
data = Data.Data()
columnIntervals = data.createColumnIntervals(minSupport,k)

for col in columnIntervals:
    for i in col:
        pass
        #print(str(i))

theData = data.loadData()

L, sup_data = ap.apriori(theData, columnIntervals, minSupport, k)

print ("L2 Data: " + str(L[1]))
#print ("Support Data: " + str(sup_data))

rules = ap.generateRules(L, sup_data, minConfidence)

for rule in rules:
    rule_str = ""
    x = rule[0]
    y = rule[1]

    for interval in x:
        rule_str += interval.hStr() + ", "

    rule_str += " --> "

    for interval in y:
        rule_str += interval.hStr() + ", "
       
    rule_str += " Confidence: " + str(rule[2])
    print(rule_str)
