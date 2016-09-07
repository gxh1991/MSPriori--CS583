import re

parameterTextFileName = 'parameter-file.txt'
inputFile = 'input-data.txt'

mis = {}  # dictionary that holds key=item value=mis
cannotBeTogether = []  # 2 dimension list contains items that cannot be together
mustHave = []  # must have list
sdc = 0  # support difference constraint
transactions = []  # transactions 2-d list
items = []  # item list in original order. Useful?
itemsSorted = []  # sorted items by their mis value
itemSetsCount = {}


def getParameterFromFile(Filename):
    global mis, cannotBeTogether, mustHave, minsup
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
                strTmp = list(map(int, strTmp))
                cannotBeTogether.append(strTmp)
        if matchMustHave:
            have = matchMustHave.group(1)
            for s in have.split('or'):
                mustHave.append(s.strip())
    parameterText.close()


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
    global itemSetsCount
    count = 0
    for t in _transactions:
        t = set(t)
        if item in t:
            if item in itemCount:
                itemSetsCount[item] += 1
                count += 1
            else:
                itemSetsCount[item] = 1
                count += 1
    return count / len(_transactions)


def init_pass(_itemsSorted, _mis):
    global transactions
    L = []
    for item in _itemsSorted:
        if(mis[item] <= getSupport(item, transactions)):
            L.append(item)
    return L


def level2_Candidate_Gen(_itemsSorted, _sdc):
    global itemSetsCount, transactions
    c2 = []
    for i in range(len(_itemsSorted)):
        item = _itemsSorted[i]
        if(itemSetsCount[item] >= mis[item]):
            for j in range(i + 1, len(_itemsSorted)):
                item2 = _itemsSorted[j]
                if(abs((itemSetsCount[item1] - itemSetsCount[item2]) / len(transactions)) <= _sdc):
                    c2.append([item, item2])


def msCandidate_Gen(f,_sdc):
    for i in range(len(f)):
        for j in range(i+1,len(f)):


def isDifferOne(f1, f2):
    if(len(f1) != len(f2)):
        return False
    for i in range(len(f1) - 1):
        if(f1[i] != f2[i]):
            return False
    if(f1[len(f1) - 1] == f2[len(f1) - 1]):
        print("Error: f1 and f2 are exactly the same!!! Check function isDifferOne(f1,f2)")
        return False


# ---------------------------------------------------------------------
#                           pre-prosessing
# --------------------------------------------------------------------
getParameterFromFile(parameterTextFileName)
getInputFromFile(inputFile)
items = getItems()
itemsSorted = sortItem(mis)
# ---------------------------------------------------------------------

F = init_pass(itemsSorted, mis)
k = 2
while F:
    if k = 2:
        c = level2_Candidate_Gen(itemsSorted,sdc)
    else:
        c = 