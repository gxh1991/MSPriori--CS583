import re

parameterTextFileName = 'parameter-file.txt'
inputFile = 'input-data.txt'

mis = {}  # dictionary that holds key=item value=mis
cannotBeTogether = []  # 2 dimension list contains items that cannot be together
mustHave = []  # must have list
minsup = 0  # min support specified manually
transactions = []  # transactions 2-d list
items = []  # item list in original order. Useful?
itemsSorted = []  # sorted items by their mis value


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
            minsup = float(matchSDC.group(1))
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
    inputText = open(Filename)
    for line in inputText:
        transactions.append(line.strip('\n').strip('{').strip('}')
                            .strip().replace(' ', '').split(','))


def getItems():
    global transactions
    for transaction in transactions:
        for item in transaction:
            items.append(item)
    return set(items)


def sortItem(mis):
    return sorted(mis, key=mis.get)


def init_pass(_itemsSorted, _mis):
    for item in _itemsSorted:
        if(mis[item] > )


# ---------------------------------------------------------------------
#                           pre-prosessing
# --------------------------------------------------------------------
getParameterFromFile(parameterTextFileName)
getInputFromFile(inputFile)
items = getItems()
itemsSorted = sortItem(mis)
# ---------------------------------------------------------------------

L = init_pass(itemsSorted, mis)
