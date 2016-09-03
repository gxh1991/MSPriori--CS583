import re

parameterTextFileName = 'parameter-file.txt'
dict = {}

parameterText = open(parameterTextFileName)
for line in parameterText:
    matchMIS = re.search('\S*\((\d*)\)\D*(\d\.?\d*)', line)
    matchSDC = re.search('SDC\D*(\d\.?\d*)', line)
    if matchMIS:
        dict[matchMIS.group(1)] = matchMIS.group(2)
    if matchSDC:
        print(matchSDC.group(1))
