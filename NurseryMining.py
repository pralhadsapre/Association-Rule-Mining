import sys
import math
import copy
import ItemSetGenerator as isg
import RuleMiner as rm
import FileReader as fr

sparseMatrix = {}
supportThres = float(sys.argv[2])
columns = ['parents', 'has_nurs', 'form', 'children', 'housing', 'finance', 'social', 'health', 'classAttr']

sparseMatrix = fr.readFile(sys.argv[1], columns)
# k_ItemSets = isg.generateCandidatesFk_1x1(sparseMatrix, supportThres)
k_ItemSets = isg.generateCandidatesFk_1xk_1(sparseMatrix, supportThres)

rules = rm.startRuleBuilding(sparseMatrix[0], k_ItemSets)
# printSomeData(sparseMatrix, 20)