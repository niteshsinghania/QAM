# -*- coding: utf-8 -*-
"""
Created on Thu Oct 09 13:46:27 2014

@author: Marcel Caraciolo
For more information on this file see:
http://aimotion.blogspot.ca/2013/01/machine-learning-and-data-mining.html

"""

import arff
import numpy as np



commonWords = ['W0','W1']

interesting = 0


def createC1(dataset):
    "Create a list of candidate item sets of size one."
    c1 = []
    for transaction in dataset:
        for item in transaction:
            if not [item] in c1:
                c1.append([item])
    c1.sort()
    #frozenset because it will be a ket of a dictionary.
    return map(frozenset, c1)
 
 
def scanD(dataset, candidates, min_support):
    "Returns all candidates that meets a minimum support level"
    sscnt = {}
    for tid in dataset:
        for can in candidates:
            if can.issubset(tid):
                sscnt.setdefault(can, 0)
                sscnt[can] += 1
 
    num_items = float(len(dataset))
    retlist = []
    support_data = {}
    for key in sscnt:
        support = sscnt[key] / num_items
        if support >= min_support:
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
                retList.append(freq_sets[i] | freq_sets[j])
    return retList
 
 
def apriori(dataset, minsupport=0.5):
    "Generate a list of candidate item sets"
    C1 = createC1(dataset)
    D = map(set, dataset)
    L1, support_data = scanD(D, C1, minsupport)
    L = [L1]
    k = 2
    while (len(L[k - 2]) > 0):
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = scanD(D, Ck, minsupport)
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
            #print "freqSet", freqSet, 'H1', H1
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
        suppX = support_data[freqSet - conseq]
        suppY = support_data[conseq]

        conf = xUniony / suppX
        lift = conf / suppY
        interest = xUniony / (suppX * suppY)
        ps = xUniony - (suppX * suppY)
        coeff = ps /((suppX*(1-suppX))*(suppY*(1-suppY)))**(0.5)
        
        #Filter out rules that are less interesting (Q5)
        if conf >= min_confidence:
            if(interesting == 1 and lift >= 3 and interest >= 3 and coeff >= 0.2 and ps >= 0.001):
                print '(',", ".join(freqSet - conseq),')', '--->', '(',",".join(conseq),')','\n', 'Conf:', conf,'\n','Lift:',lift,'\n','Interest:',interest,'\n','PS:',ps,'\n','Coefficient:', coeff,'\n'
                rules.append((freqSet - conseq, conseq, conf))
                pruned_H.append(conseq)

            if (interesting == 0):
                set1 = list (freqSet-conseq)
                set2 = list (conseq)
                checker = None
                for i in range(len(set1)):
                    if (set1[i] == 'W2'):
                        checker = True
                for i in range(len(set2)):
                    if (set2[i] == 'W2'):
                        checker = True

                if  (checker == True):
                    print '(',", ".join(freqSet - conseq),')', '--->', '(',",".join(conseq),')','\n', 'Conf:', conf,'\n','Lift:',lift,'\n','Interest:',interest,'\n','PS:',ps,'\n','Coefficient:', coeff,'\n'
                rules.append((freqSet - conseq, conseq, conf))
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
            
            
############################################

    