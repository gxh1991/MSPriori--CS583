import re

parameterTextFileName = 'parameter-file.txt'
inputFile = 'input-data.txt'

mis = {}  # dictionary that holds key=item value=mis
cannotBeTogether = []  # list contains items that cannot be together
cannotBeTogetherSets = []
mustHave = []  # must have list
sdc = 0  # support difference constraint
transactions = []  # transactions 2-d list
items = []  # item list in original order. Useful?
itemsSorted = []  # sorted items by their mis value
itemSetsCount = {}
itemSetsCountFinal = {}
itemSetsTailCount = {}
numberOfTransaction = 0


def getParameterFromFile(Filename):
    global mis, cannotBeTogether, mustHave, minsup, sdc
    parameterText = open(Filename)
    for line in parameterText:
        matchMIS = re.search('\S*\((\d*)\)\D*(\d\.?\d*)', line)
        matchSDC = re.search('SDC\D*(\d\.?\d*)', line)
        matchTogether = re.search('cannot_be_together: {(.*)}', line)
        matchMustHave = re.search('must-have: (.*)', line)
        if matchMIS:
            mis[int(matchMIS.group(1))] = float(matchMIS.group(2))
        if matchSDC:
            sdc = float(matchSDC.group(1))
        if matchTogether:
            togetherTmp = matchTogether.group(1)
            tmp = togetherTmp.replace('{', '').replace(
                '}', '').replace(' ', '').split('and')
            for str in tmp:
                strTmp = str.split(',')
                cannotBeTogether = list(map(int, strTmp))
        if matchMustHave:
            have = matchMustHave.group(1)
            for s in have.split('or'):
                mustHave.append(int(s.strip()))
    parameterText.close()


def isListContains(_sub, _list):
    if(isinstance(_sub, list)):
        for item in _sub:
            if item not in _list:
                return False
    else:
        if _sub not in _list:
            return False
    return True


def getInputFromFile(Filename):
    global transactions
    transactionsTmp = []
    inputText = open(Filename)
    for line in inputText:
        transactionsTmp = line.strip('\n').replace(
            '{', '').replace('}', '').strip().replace(' ', '').split(',')
        transactions.append(list(map(int, transactionsTmp)))


def getItems():
    global transactions
    for transaction in transactions:
        for item in transaction:
            items.append(item)
    return set(items)


def sortItem(mis):
    return sorted(mis, key=mis.get)


def getSupport(item, _transactions):
    count = 0
    for t in _transactions:
        t = set(t)
        if item in t:
            count += 1
    return count / len(_transactions)


def getItemsSupport(itemSet):
    global transactions
    itemsCount = {}
    for item in itemSet:
        count = 0
        for t in transactions:
            if(isListContains(item, t)):
                count += 1
        itemsCount[item] = count
    return count


def init_pass(_itemsSorted, _mis):
    global transactions, itemSetsCount, itemSetsCountFinal
    L = []
    for item in _itemsSorted:
        itemSetsCount[item] = getSupport(
            item, transactions) * len(transactions)
        tmpList = []
        tmpList.append(item)
        itemSetsCountFinal[tuple(tmpList)] = int(itemSetsCount[item])
        if(mis[item] <= getSupport(item, transactions)):
            tmp = []
            tmp.append(item)
            L.append(tmp)
    return L


def level2_Candidate_Gen(_itemsSorted, _sdc):
    global itemSetsCount, transactions
    c2 = []
    for i in range(len(_itemsSorted)):
        item = _itemsSorted[i]
        if(itemSetsCount[item] / numberOfTransaction >= mis[item]):
            for j in range(i + 1, len(_itemsSorted)):
                item2 = _itemsSorted[j]
                if(abs((itemSetsCount[item] - itemSetsCount[item2]) / len(transactions)) <= _sdc):
                    c2.append([item, item2])
    return c2


def getK_1Subsets(candidate):
    result = []
    for c in candidate:
        lst = list(candidate)
        lst.remove(c)
        result.append(lst)
    return result


def msCandidate_Gen(f, _sdc):
    c = []
    c_small = []
    for i in range(len(f)):
        for j in range(i + 1, len(f)):
            if isDifferOne(f[i], f[j]) and abs(getItemsSupport(f[i]) - getItemsSupport(f[j])) / numberOfTransaction <= sdc:
                tmp = list(f[i])
                tmp.append(f[j][-1])
                c_small = tmp
                c.append(c_small)
                subsets = getK_1Subsets(c_small)
                for subset in subsets:
                    if(c_small[0] in subset) or (mis[c_small[0]] == mis[c_small[1]]):
                        if subset not in frequentSets:
                            if c_small in c:
                                c.remove(c_small)
    return c


def isDifferOne(f1, f2):
    if(len(f1) != len(f2)):
        return False
    for i in range(len(f1) - 1):
        if(f1[i] != f2[i]):
            return False
    if(f1[len(f1) - 1] == f2[len(f1) - 1]):
        print("Error: f1 and f2 are exactly the same!!! Check function isDifferOne(f1,f2)")
        return False
    return True


def getPairSets(_cannotBeTogether):
    _cannotBeTogether = sortListByMis(_cannotBeTogether)
    result = []
    for i in range(0, len(_cannotBeTogether) - 1):
        for j in range(i + 1, len(_cannotBeTogether)):
            tmp = [_cannotBeTogether[i], _cannotBeTogether[j]]
            result.append(tmp)
    return result


def sortListByMis(l):
    global itemsSorted
    return sorted(l, key=itemsSorted.index)


def mustHaveFilter(itemSets):
    global mustHave
    removes = []
    for i in itemSets:
        haveFlg = False
        for j in mustHave:
            if j in i:
                haveFlg = True
                break
        if not haveFlg:
            removes.append(i)
    for i in removes:
        itemSets.remove(i)


def cannotBetogetherFilter(itemSets):
    global cannotBeTogetherSets
    removes = []
    for i in itemSets:
        for j in cannotBeTogetherSets:
            if isListContains(j, i):
                removes.append(i)
                break
    for i in removes:
        itemSets.remove(i)

# ---------------------------------------------------------------------
#                           pre-prosessing
# --------------------------------------------------------------------
getParameterFromFile(parameterTextFileName)
getInputFromFile(inputFile)
items = getItems()
itemsSorted = sortItem(mis)
numberOfTransaction = len(transactions)
cannotBeTogetherSets = getPairSets(cannotBeTogether)
mustHave = sortListByMis(mustHave)
# ---------------------------------------------------------------------

F = init_pass(itemsSorted, mis)

k = 2
frequentSets = []
frequentSets2 = []
while F:
    frequentSets += list(F)
    frequentSets2.append(F)
    if k == 2:
        candidates = level2_Candidate_Gen(itemsSorted, sdc)
    else:
        candidates = msCandidate_Gen(F, sdc)
    k += 1
    F = []
    for c in candidates:
        count = 0
        count2 = 0
        tmp = list(c)
        tmp.remove(tmp[0])
        for t in transactions:
            if(isListContains(c, t)):
                count += 1
            if(isListContains(tmp, t)):
                count2 += 1
        # since list cannot be a key of a dictionary, i replaced it by tuple. N
        itemSetsCountFinal[tuple(c)] = count
        itemSetsTailCount[tuple(c)] = count2  # this line too!!!!
        if(count / numberOfTransaction >= mis[c[0]]):
            F.append(c)

mustHaveFilter(frequentSets)
cannotBetogetherFilter(frequentSets)

for i in frequentSets2:
    mustHaveFilter(i)
    cannotBetogetherFilter(i)


print(frequentSets)

# --------------------------------------------------------------------------
# Generating output
# --------------------------------------------------------------------------


# class OutputPattern:
#     sizeOfFrequenSet = 0
#     frequentSet = []
#     frequenctCount = []
#     frequenctTailCount = []

#     def addItemSet(self, _itemSet, _count, _tailCount):
#         self.frequentSet.append(_itemSet)
#         self.frequenctCount.append(_count)
#         self.frequenctTailCount.append(_tailCount)
#         self.sizeOfFrequenSet = len(_itemSet)

#     def fixBracet(str):
#         return str.replace('(', '{').replace(')', '}')

#     def getOutput(self):
#         result = ''
#         if self.sizeOfFrequenSet == 0:
#             return
#         else:
#             result += 'Frequent ' + str(self.sizeOfFrequenSet) + '-itemsets\n'
#             for i in range(frequentSets):
#                 result += '\t'
#                 result += str(frequenctCount[i]) + ' ' + ': ' + 


