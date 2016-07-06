import sys
import math
import copy
import ItemSetGenerator as isg
import RuleMiner as rm
import FileReader as fr

sparseMatrix = {}
supportThres = float(sys.argv[2])
columns = ['age', 'wife education','husband education','Number of children', 'wife religion', 
			'wife working', 'husband occupation', 'Standard-of-living', 'Media exposure', 'Contraceptive method']
sparseMatrix = fr.readFile(sys.argv[1], columns)
# fr.printSomeData(sparseMatrix, 20)
k_ItemSets = isg.generateCandidatesFk_1xk_1(sparseMatrix, supportThres)

rules = rm.startRuleBuilding(sparseMatrix[0], k_ItemSets)

# k_ItemSets = isg.generateCandidatesFk_1x1(sparseMatrix, supportThres)
# rules = rm.startRuleBuilding(sparseMatrix[0], k_ItemSets)
