from csv import reader
from collections import defaultdict
from itertools import chain, combinations

itemSetList =  [['eggs', 'bacon', 'soup'],
                ['eggs', 'bacon', 'apple'],
                ['soup', 'bacon', 'banana']]

tempItemSet = set()

for itemSet in itemSetList:
    for item in itemSet:
        tempItemSet.add(frozenset([item]))

print(tempItemSet)

freqItemSet = set()
localItemSetWithSup = defaultdict(int)

for item in tempItemSet:
    for itemSet in itemSetList:
        if item.issubset(itemSet):
            localItemSetWithSup[item] += 1

for item, supCount in localItemSetWithSup.items():
    support = float(supCount / len(itemSetList))
    if (support >= 0.5):
        freqItemSet.add(item)

print(freqItemSet)

freqItemSet_new = set()
#print(set([i.union(j) for i in freqItemSet for j in freqItemSet if len(i.union(j)) == 2]))
for i in freqItemSet:
    for j in freqItemSet:
        if len(i.union(j)) == 2:
            freqItemSet_new.add(i.union(j))

print(freqItemSet_new)

tempCandidateSet = freqItemSet_new.copy()
for item in freqItemSet_new:
    subsets = combinations(item, 2)
    for subset in subsets:
        # if the subset is not in previous K-frequent get, then remove the set
        if (frozenset(subset) not in freqItemSet):
            tempCandidateSet.remove(item)
            break;

print(tempCandidateSet)