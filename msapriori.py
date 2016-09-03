import re

parameterTextFileName = 'parameter-file.txt'
dict = {}
cannotBeTogether = []
mustHave = []
minsup = 0


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

