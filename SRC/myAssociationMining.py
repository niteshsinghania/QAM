# -*- coding: utf-8 -*-

# Imports
import apriorialg as ap
import Data

maxSupport = 0.5
minSupport = 0.4
minConfidence = 0.7
K = 19
R = 4

# Read the data
columnNames = ['W','L','R','AB','H','2B','3B','HR','BB','SO','SB','RA','ER','ERA','HA','HRA','BBA','SOA','E']
tableName = ['Teams']

data = Data.Data(columnNames,tableName[0])
columnIntervals = data.createColumnIntervals(minSupport,K)

theData = data.loadData()

L, sup_data = ap.apriori(theData, columnIntervals,columnNames, minSupport, maxSupport, K)


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
    rule_str += "\n"
    rule_str += " Confidence: " + str(rule[2][0])
    rule_str += "\n"
    rule_str += " Interest: " + str(rule[2][1])
    rule_str += "\n"
    rule_str += " PS: " + str(rule[2][3])
    rule_str += "\n"
    rule_str += " CoEff: " + str(rule[2][4])
    print(rule_str)

