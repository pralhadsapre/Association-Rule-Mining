# python script to convert classification data set to sparse matrix association transaction data
import sys
import math
import copy
import ItemSetGenerator as isg
import RuleMiner as rm
import FileReader as fr


sparseMatrix = {}
supportThres = float(sys.argv[2])
columns = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class']
sparseMatrix = fr.readFile(sys.argv[1], columns)
# fr.printSomeData(sparseMatrix, 20)
k_ItemSets = isg.generateCandidatesFk_1xk_1(sparseMatrix, supportThres)
# k_ItemSets = isg.generateCandidatesFk_1x1(sparseMatrix, supportThres)
rules = rm.startRuleBuilding(sparseMatrix[0], k_ItemSets)
