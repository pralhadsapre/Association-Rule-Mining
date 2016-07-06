import math
import copy
import ItemSet as itemset

def countSupport(sparseMatrix, itemSet):
	candidate = itemSet.getItems()
	support = 0.0
	for i in range(1, len(sparseMatrix)):
		count = 0
		for j in range(len(candidate)):
			if sparseMatrix[i][candidate[j]] == True:
				count += 1
			else:
				break

		if count == len(candidate):
			support += 1

	support /= len(sparseMatrix)
	itemSet.setSupport(support)
	return support

def checkDuplicate(k_ItemSets, candidate):
	if len(candidate.getItems()) in k_ItemSets:
		for item in k_ItemSets[len(candidate.getItems())]:
			if item.equals(candidate):
				return True

	return False

def addCandidate(sparseMatrix, k_ItemSets, candidate, kValue, parent1, parent2, minSupport):
	global frequentItemSets
	global generatedItemSets	

	if candidate != None:
		# print candidate.getItems()
		if not checkDuplicate(k_ItemSets[kValue], candidate):
			generatedItemSets += 1
			support = countSupport(sparseMatrix, candidate)			
			# print "Found support of %d for %s candidate against minSupport of %d" % (support, str(candidate.getItems()), minSupport)
			
		if support >= minSupport:			
			# print ".",
			parent1.setMaximalFrequent(False)
			parent2.setMaximalFrequent(False)

			if support == parent1.getSupport():
				parent1.setClosedFrequent(False)
			if support == parent2.getSupport():
				parent2.setClosedFrequent(False)

			k_ItemSets[kValue].append(copy.copy(candidate))
			frequentItemSets += 1

def printItemSets():
	global k_ItemSets

	print "Here are the generated candidates"
	print "-" * 90
	for x in k_ItemSets:
		for item in k_ItemSets[x]:
			print item.getItems(),
		print "\n" + ("-" * 90)

def getStatistics(k_ItemSets):
	totalFreqCount = 0
	maximalFreqCount = 0
	closedFreqCount = 0

	maxFreqString = ""
	closedFreqString = ""

	for x in k_ItemSets:
		for item in k_ItemSets[x]:
			totalFreqCount += 1			
			if item.getIsMaximalFrequent():
				maxFreqString += (str(item.getItems()) + " ")
				maximalFreqCount += 1				
			
			if item.getIsClosedFrequent():
				closedFreqString += (str(item.getItems()) + " ")
				closedFreqCount += 1

	# print maxFreqString
	# print closedFreqString
	print "%d items are frequent" % totalFreqCount
	print "%d items are closed frequent" % closedFreqCount
	print "%d items are maximal frequent" % maximalFreqCount


def generateCandidatesFk_1x1(sparseMatrix, supportThres):
	minSupportCount = (float(supportThres) / 100)

	global generatedItemSets
	global frequentItemSets
	global k_ItemSets

	generatedItemSets = 0
	frequentItemSets = 0
	
	# print minSupportCount	
	k_ItemSets = {}

	k_ItemSets[1] = []
	for x in range(len(sparseMatrix[0])):
		candidate = []
		candidate.append(x)
		item = itemset.ItemSet(candidate)		
		generatedItemSets += 1
		if countSupport(sparseMatrix, item) >= minSupportCount:
			k_ItemSets[1].append(item)
			frequentItemSets += 1

	if len(k_ItemSets[1]) > 1:
		for i in range(2, len(sparseMatrix[0])):
			k_ItemSets[i] = []

			if len(k_ItemSets[i - 1]) < 2:
				break

			for j in k_ItemSets[i - 1]:
				for k in k_ItemSets[1]:					
					candidate = j.merge(k, 1)
					
					addCandidate(sparseMatrix, k_ItemSets, candidate, i, j, k, minSupportCount)
					
			# printK_ItemSet(k_ItemSets[i])
			print "%d-frequent k_ItemSets generated" % i

	# printItemSets()
	print "%s item sets were generated" % generatedItemSets	
	print "Method used was Fk-1x1"
	getStatistics(k_ItemSets)
	return k_ItemSets

def generateCandidatesFk_1xk_1(sparseMatrix, supportThres):
	minSupportCount = (float(supportThres) / 100)
	# print minSupportCount

	global generatedItemSets
	global frequentItemSets
	global k_ItemSets

	generatedItemSets = 0
	frequentItemSets = 0
	k_ItemSets = {}

	k_ItemSets[1] = []
	for x in range(len(sparseMatrix[0])):
		candidate = []
		candidate.append(x)
		item = itemset.ItemSet(candidate)		
		generatedItemSets += 1
		if countSupport(sparseMatrix, item) >= minSupportCount:
			k_ItemSets[1].append(item)
			frequentItemSets += 1

	# printK_ItemSet(k_ItemSets[1])

	if len(k_ItemSets[1]) > 1:

		for i in range(2, len(sparseMatrix[0])):
			k_ItemSets[i] = []

			if len(k_ItemSets[i - 1]) < 2:
				break

			for j in range(len(k_ItemSets[i - 1]) - 1):
				for k in range(j + 1, len(k_ItemSets[i - 1])):
					if i == 2:
						candidate = k_ItemSets[i - 1][j].merge(k_ItemSets[i - 1][k], 1)
					else:
						candidate = k_ItemSets[i - 1][j].merge(k_ItemSets[i - 1][k], 2)

					addCandidate(sparseMatrix, k_ItemSets, candidate, i, k_ItemSets[i - 1][j], k_ItemSets[i - 1][k], minSupportCount)					

			# printK_ItemSet(k_ItemSets[i])
			print "\n%d-frequent k_ItemSets generated" % i
		
	# printItemSets()
	print "%s item sets were generated" % generatedItemSets		
	print "Method used was Fk-1xFk-1"
	getStatistics(k_ItemSets)

	return k_ItemSets

k_ItemSets = {}
generatedItemSets = 0
frequentItemSets = 0