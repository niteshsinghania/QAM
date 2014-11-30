# -*- coding: utf-8 -*-
"""
Created on Thu Oct 09 13:46:27 2014

@author: Marcel Caraciolo
For more information on this file see:
http://aimotion.blogspot.ca/2013/01/machine-learning-and-data-mining.html

"""

import arff
import numpy as np
import Item
import Data

def scan_support(dataset, columnIntervals, min_support, k):
    sscnt = {}
    for column_index, colInt in enumerate(columnIntervals):
        for interval in colInt:
            sscnt.setdefault(interval, 0)
            for tid in dataset:
                val = tid[column_index]
                if(val >= interval.l and val <= interval.u):
                    sscnt[interval] += 1 
    
    num_trx = float(len(dataset))
    '''''
    count = 0
    for x in columnIntervals:
        for y in x:
            print(y)
            count += 1
    if len(sscnt) != count:
        print ("ERROR didn't count all data sscnt: " + str(len(sscnt)) + " column int: " + str(count))
    '''''
    retlist = []
    support_data = {}
    for key in sscnt:
        support = sscnt[key] / num_trx
        if support >= min_support:
            retlist.insert(0, frozenset([key]))
            #Generalize current interval
            if (key.u != key.l) and (key.next):
                it = key
                gen_sup = sscnt[it] / num_trx
                while(it.next):
                    it = it.next
                    if it in sscnt:
                        gen_sup += sscnt[it] / num_trx
                    else:
                        print("ERROR couldn't find" + str(it))
                    gen_item = Item.Item(key.name, key.l, it.u)
                    if (gen_sup > 1.0):
                        print("ERROR gen sup too HIGH!!")
                    if (gen_sup <= k * support):
                        retlist.insert(0, frozenset([gen_item]))
                        support_data[frozenset([gen_item])] = gen_sup
                    else:
                        break

        support_data[frozenset([key])] = support

    return retlist, support_data

def scan_support2(dataset,columnNames, candidates, minSupport):
    sscnt = {}
    for tid in dataset:
        for can in candidates:
            count = 0
            for interval in can:
                colNum = columnNames.index(interval.name)
                val = tid[colNum]
                if(val >= interval.l and val <= interval.u):
                    count += 1
            if count == len(can):
                if type(can) != type(frozenset()):
                    print("ERRORR")
                sscnt.setdefault(can, 0)
                sscnt[can] += 1

    num_trx = float(len(dataset))

    retlist = []
    support_data = {}
    for key in sscnt:
        support = sscnt[key] / num_trx
        if support >= minSupport:
            retlist.insert(0, key)

        support_data[key] = support

    return retlist, support_data

                


def aprioriGen(freq_sets, k):
    "Generate the joint transactions from candidate sets"
    retList = []
    lenLk = len(freq_sets)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(freq_sets[i])[:k - 2]
            L2 = list(freq_sets[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                s = [list(freq_sets[i])[0]]
                for inti in freq_sets[i]:
                    for ints in s:
                        if inti.name != ints.name:
                            s.append(inti)

                for intj in freq_sets[j]:
                    for ints in s:
                        if intj.name != ints.name:
                            s.append(intj)
                if(len(s) == k):
                    retList.append(frozenset(s))
    return retList
 
 
def apriori(dataset, column_intervals,columnNames, minsupport, k):
    "Generate a list of candidate item sets"
    L1, support_data = scan_support(dataset, column_intervals, minsupport, k)
    L = [L1]
   
    print("At k: 1 len of L is " + str(len(L1)))

    k = 2
    while (len(L[k - 2]) > 0):
        Ck = aprioriGen(L[k - 2], k)

        Lk, supK = scan_support2(dataset,columnNames, Ck, minsupport)
        print("At k: " + str(k) + " len of L is " + str(len(Lk)))
        support_data.update(supK)
        L.append(Lk)
        k += 1
 
    return L, support_data
 
def generateRules(L, support_data, min_confidence=0.7,interesting=0):
    """Create the association rules
    L: list of frequent item sets
    support_data: support data for those itemsets
    min_confidence: minimum confidence threshold
    """
    rules = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rules_from_conseq(freqSet, H1, support_data, rules, min_confidence)
            else:
                calc_confidence(freqSet, H1, support_data, rules, min_confidence)
    return rules


 
def calc_confidence(freqSet, H, support_data, rules, min_confidence=0.7):
    "Evaluate the rule generated"
    pruned_H = []
    for conseq in H:


        xUniony = support_data[freqSet]
        diff = []
        for f in freqSet:
            for c in conseq:
                if f.name != c.name:
                    diff.append(f)
        
        x = frozenset(diff)

        suppX = support_data[x]
        suppY = support_data[conseq]

        conf = xUniony / suppX
        lift = conf / suppY
        interest = xUniony / (suppX * suppY)
        ps = xUniony - (suppX * suppY)
        coeff = ps /((suppX*(1-suppX))*(suppY*(1-suppY)))**(0.5)
        
        #Filter out rules that are less interesting (Q5)
        if conf >= min_confidence:
                rules.append((x, conseq, [conf, lift, interest, ps, coeff]))

    return rules 
 
 
def rules_from_conseq(freqSet, H, support_data, rules, min_confidence=0.7):
    "Generate a set of candidate rules"
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calc_confidence(freqSet, Hmp1,  support_data, rules, min_confidence)
        if len(Hmp1) > 1:
            rules_from_conseq(freqSet, Hmp1, support_data, rules, min_confidence)
