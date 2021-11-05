from csv import reader
from collections import defaultdict
from itertools import chain, combinations
from optparse import OptionParser
from apriori_python.utils import *

def apriori(itemSetList, minSup, minConf):
#範例
#itemSetList =  [['eggs', 'bacon', 'soup'],
#                ['eggs', 'bacon', 'apple'],
#                ['soup', 'bacon', 'banana']]
    #抓出陣列裡每個item，{frozenset({'bacon'}), frozenset({'soup'}), frozenset({'banana'}), frozenset({'apple'}), frozenset({'eggs'})}
    C1ItemSet = getItemSetFromList(itemSetList)
    # Final result global frequent itemset
    globalFreqItemSet = dict()
    # Storing global itemset with support count
    globalItemSetWithSup = defaultdict(int) # default值以一個list()方法產生
    #取得一個L1的頻繁項集
    #{frozenset({'bacon'}), frozenset({'soup'}), frozenset({'eggs'})}
    L1ItemSet = getAboveMinSup(
        C1ItemSet, itemSetList, minSup, globalItemSetWithSup)
    currentLSet = L1ItemSet
    k = 2
    # Calculating frequent item set
    # 當候選項集不為空時
    while(currentLSet):
        # Storing frequent itemset
        #取得當下大於最小支持度的頻繁項集
        globalFreqItemSet[k-1] = currentLSet
        # Self-joining Lk
        #取得候選K項集，假如k=2，則{frozenset({'eggs', 'soup'}), frozenset({'soup', 'bacon'}), frozenset({'eggs', 'bacon'})}
        candidateSet = getUnion(currentLSet, k)
        # Perform subset testing and remove pruned supersets
        # 去除當前的候選項集不存在在上一層的項集裡，例如:目前計算出2 item項集，也就是{frozenset({'eggs', 'soup'}), frozenset({'soup', 'bacon'}), frozenset({'eggs', 'bacon'})}
        # 裡面的個別item需要存在在k=1項集裡，以此類推，也就是如果在計算3 item 項集，要去比對計算出的候選項集是否都有存在在2 item項集裡
        candidateSet = pruning(candidateSet, currentLSet, k-1)
        # Scanning itemSet for counting support
        # 候選項集必須大於最小支持度
        currentLSet = getAboveMinSup(
            candidateSet, itemSetList, minSup, globalItemSetWithSup)
        k += 1
    # 列出每個associationRule
    rules = associationRule(globalFreqItemSet, globalItemSetWithSup, minConf)

    # 以confidence排序
    rules.sort(key=lambda x: x[2])

    return globalFreqItemSet, rules

def aprioriFromFile(fname, minSup, minConf):
    C1ItemSet, itemSetList = getFromFile(fname)

    # Final result global frequent itemset
    globalFreqItemSet = dict()
    # Storing global itemset with support count
    globalItemSetWithSup = defaultdict(int)

    L1ItemSet = getAboveMinSup(
        C1ItemSet, itemSetList, minSup, globalItemSetWithSup)
    currentLSet = L1ItemSet
    k = 2

    # Calculating frequent item set
    while(currentLSet):
        # Storing frequent itemset
        globalFreqItemSet[k-1] = currentLSet
        # Self-joining Lk
        #抓出候選的項集
        candidateSet = getUnion(currentLSet, k)
        # Perform subset testing and remove pruned supersets
        candidateSet = pruning(candidateSet, currentLSet, k-1)
        # Scanning itemSet for counting support
        currentLSet = getAboveMinSup(
            candidateSet, itemSetList, minSup, globalItemSetWithSup)
        k += 1

    rules = associationRule(globalFreqItemSet, globalItemSetWithSup, minConf)
    rules.sort(key=lambda x: x[2])

    return globalFreqItemSet, rules

if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='inputFile',
                         help='CSV filename',
                         default=None)
    optparser.add_option('-s', '--minSupport',
                         dest='minSup',
                         help='Min support (float)',
                         default=0.5,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minConf',
                         help='Min confidence (float)',
                         default=0.5,
                         type='float')

    (options, args) = optparser.parse_args()

    freqItemSet, rules = aprioriFromFile(options.inputFile, options.minSup, options.minConf)