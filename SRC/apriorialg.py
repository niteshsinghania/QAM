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

# Generalize intervals by combing adjact partitions 
# stopping when support is above max support
def generalize_intervals(support_data, min_support, max_support):
    gen_list = []
    gen_support_data = {}
    for fSet in support_data:
        o_it = it = list(fSet)[0]
        if (it.u != it.l) and (it.next):
            while(it.next):
                it = it.next
                
                gen_item = Item.Item(o_it.name, o_it.l, it.u)

                gen_list.insert(0, frozenset([gen_item]))

    return gen_list


def scan_support(dataset, columnIntervals, min_support, max_support):
    sscnt = {}
    for column_index, colInt in enumerate(columnIntervals):
        for interval in colInt:
            sscnt.setdefault(interval, 0)
            for tid in dataset:
                val = tid[column_index]
                if(val >= interval.l and val <= interval.u):
                    sscnt[interval] += 1 
    
    num_trx = float(len(dataset))
    retlist = []
    support_data = {}
    for key in sscnt:
        support = sscnt[key] / num_trx
        if support >= min_support:
            retlist.insert(0, frozenset([key]))
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

                


def aprioriGen(freq_sets, k, pruning=False):
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
                    match = False
                    for ints in s:
                        if inti.name == ints.name:
                            match = True
                            break
                    if not match:
                        s.append(inti)

                for intj in freq_sets[j]:
                    match = False
                    for ints in s:
                        if intj.name == ints.name:
                            match = True
                            break
                    if not match:
                        s.append(intj)
                s_str = ""
                for interval in s:
                    s_str += interval.hStr() + ", "
                if(len(s) == k):
                    if pruning and k > 2:
                        for fs in freq_sets:
                            if (set(fs).issubset(s)):
                                retList.append(frozenset(s))
                                break
                    else:
                        retList.append(frozenset(s))

    return retList
 
 
def apriori(dataset, column_intervals,columnNames, min_support, max_support, R):
    "Generate a list of candidate item sets"
    L1, support_data = scan_support(dataset, column_intervals, min_support, max_support)
    Lgeneralized = generalize_intervals(support_data, min_support, max_support)
    print("Created " + str(len(Lgeneralized)) + " generalized intervals")
    Lg, sup_data = scan_support2(dataset, columnNames, Lgeneralized, min_support)

    #Filter generaliztions greater than max_support
    for fSet in Lg:
        if sup_data[fSet] > max_support:
            Lg.remove(fSet)
    L1 += Lg
    support_data.update(sup_data)

    #Filter candidates whose support is greater than 1/R
    if R > 0:
        for fSet in L1:
            for item in fSet:
                if support_data[frozenset([item])] > 1/float(R):
                   L1.remove(fSet) 
    L = [L1]
   
    print("At k: 1 len of L is " + str(len(L1)))

    k = 2
    while (len(L[k - 2]) > 0):
        Ck = aprioriGen(L[k - 2], k, pruning=True)
        Lk, supK = scan_support2(dataset,columnNames, Ck, min_support)
        support_data.update(supK)
        L.append(Lk)
        print("At k: " + str(k) + " len of L is " + str(len(Lk)))

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
        print("Calculating consequene for L" + str(i))
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
            found = False
            for c in conseq:
                if f.name == c.name:
                    found = True
            if found == False:
                    diff.append(f)
    
        x = frozenset(diff)
        

        suppX = support_data[x]
        suppY = support_data[conseq]
        conv = 0
        conf = xUniony / suppX
        lift = conf / suppY
        ps = xUniony - (suppX * suppY)
        if (conf != 1):
            conv = (1 - suppY ) / (1 - conf)
        
        #Filter out rules that are less interesting (Q5)
        if conf >= min_confidence:
            rules.append((x, conseq, [conf, lift, ps, conv]))
            pruned_H.append(conseq)

    return pruned_H 
 
 
def rules_from_conseq(freqSet, H, support_data, rules, min_confidence=0.7):
    "Generate a set of candidate rules"
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calc_confidence(freqSet, Hmp1,  support_data, rules, min_confidence)
        if len(Hmp1) > 1:
            rules_from_conseq(freqSet, Hmp1, support_data, rules, min_confidence)
