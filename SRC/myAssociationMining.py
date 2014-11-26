# -*- coding: utf-8 -*-

# Imports
import apriorialg as ap
import myKMeans as km

# turn filter on/off
# Data filter (Q7)
filter = 0



# Read the data (Q1)
dataset = km.load_dataset()


# When you get to part 7. you might wish to come back and
# filter the data here - you could optionally have a variable
# that is a flag to turn this filtering on and off

if (filter == 0):

    minSupport = 0.05
    minConfidence = 0.7
    
    # Intresting rules filter (Q5)
    ap.interesting = 0

    if (ap.interesting == 0):
        print ''
        print 'Original Rules:'
        
        #(Q2)
        # Find frequent itemsets - consider apriorialg.py
        L,supportData= ap.apriori(dataset,minSupport)
        
        #(Q3)
        # Generate rules - consider apriorialg.py
        rules = ap.generateRules(L,supportData,minConfidence)
        print 'Total Rules: ', len(rules)

    
    if (ap.interesting == 1):
        print ''
        print 'Interesting Rules:'
    
        #(Q2)
        # Find frequent itemsets - consider apriorialg.py
        L,supportData= ap.apriori(dataset,minSupport)
    
        #(Q3)
        # Generate rules - consider apriorialg.py
        rules = ap.generateRules(L,supportData,minConfidence)
        print 'Total Rules: ', len(rules)

if (filter == 1):
    
    minSupport = 0.1
    minConfidence = 0.7
    
    # Intresting rules filter (Q5)
    ap.interesting = 0

    
    # Generate interesting rules (Lift,Interest, PS, Phi)
    print ''
    print 'Filtered Rules:'
    
    # Find frequent itemsets - consider apriorialg.py
    L,supportData= ap.apriori(dataset,minSupport)
    
    # Generate rules - consider apriorialg.py
    rules = ap.generateRules(L,supportData,minConfidence)

        
        
        
