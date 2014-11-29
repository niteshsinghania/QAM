# -*- coding: utf-8 -*-

# Imports
import apriorialg as ap
import Data

minSupport = 0.02
minConfidence = 0.001
k = 10

#minSupport = 0.1
#minConfidence = 0.001
#k = 20

#minSupport = 0.25
#minConfidence = 0.001
#k = 5

# Read the data
data = Data.Data()
columnIntervals = data.createColumnIntervals(minSupport,k)

for col in columnIntervals:
    for i in col:
        pass
        #print(str(i))

theData = data.loadData()

L, sup_data = ap.apriori(theData, columnIntervals, minSupport, k)


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
       
    rule_str += " Confidence: " + str(rule[2][0])
    rule_str += " Interest: " + str(rule[2][1])
    rule_str += " PS: " + str(rule[2][3])
    rule_str += " CoEff: " + str(rule[2][4])
    print(rule_str)

