import re

parameterTextFileName = 'parameter-file.txt'
inputFile = 'input-data.txt'

dict = {}
cannotBeTogether = []
mustHave = []
minsup = 0
transactions = []
items = []


def getParameterFromFile(Filename):
    global dict, cannotBeTogether, mustHave, minsup
    parameterText = open(Filename)
    for line in parameterText:
        matchMIS = re.search('\S*\((\d*)\)\D*(\d\.?\d*)', line)
        matchSDC = re.search('SDC\D*(\d\.?\d*)', line)
        matchTogether = re.search('cannot_be_together: {(.*)}', line)
        matchMustHave = re.search('must-have: (.*)', line)
        if matchMIS:
            dict[matchMIS.group(1)] = matchMIS.group(2)
        if matchSDC:
            minsup = matchSDC.group(1)
        if matchTogether:
            together = matchTogether.group(1)
            cannotBeTogether.append(together.split(','))
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
    global items, transactions
    for transaction in transactions:
        for item in transaction:
            items.append(item)
    items = set(items)
getParameterFromFile(parameterTextFileName)
getInputFromFile(inputFile)
