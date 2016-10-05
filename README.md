# Msapriori--CS583
This is the course project1  for CS583, University of Illinois at Chicago. 

Implement: Msapriori (excluding rule generation)
Consider: multiple minimum supports, support difference constraint, and item constraints

Item constraints: Two types
1.Cannot–be-together: sets of items cannot be in the same itemsets (pairwise), 
e.g., {1, 2, 3} and {6, 7, 9 10}
2.Must-have: every itemset must have, 
e.g., (1 or 2)

The paper of Msapriori can be found on http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.80.4877&rep=rep1&type=pdf
The instruction of the project can be found here: http://www.cs.uic.edu/~liub/teach/cs583-fall-16/CS583-association-sequential-patterns.ppt (page 46)


How to run:
1.change the 'parameterTextFileName' and 'inputFile' path variable in msapriori.py file.
 -- test data files are in data directory
2. run python3 msapriori.py. Frequent sets will be printed in terminal. Output file will be generated in the same directory of msapriori.py
