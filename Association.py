# python script to convert classification data set to sparse matrix association transaction data
import sys
import math
import copy

def readFile(fileName, sparseMatrix):
	columns = ['parents', 'has_nurs', 'form', 'children', 'housing', 'finance', 'social', 'health', 'classAttr']

	dataFile = open(fileName, 'r')	
	uniqueValues = None

	for line in dataFile:
		data = line.split(',')		
		data[len(data) - 1] = data[len(data) - 1].split('\n', 2)[0]
					
		# intializing the unique value dictionary
		if uniqueValues == None:
			uniqueValues = {}
			for x in range(len(data)):
				uniqueValues[x] = []

		for x in range(len(data)):
			if data[x] not in uniqueValues[x]:
				uniqueValues[x].append(data[x]);

	totalColumns = 0
	starts = []
	for x in range(len(uniqueValues)):
		starts.append(totalColumns)
		totalColumns += len(uniqueValues[x])
		print uniqueValues[x]
	
	# print "Total Columns is %d" % totalColumns
	dataFile.seek(0)

	counter = 0
	sparseMatrix[counter] = []
	for i in range(len(uniqueValues)):		
		for j in range(len(uniqueValues[i])):
			sparseMatrix[counter].append(str(columns[i] + "(" + uniqueValues[i][j] + ")" ))

	counter += 1
	for line in dataFile:
		data = line.split(',')		
		data[len(data) - 1] = data[len(data) - 1].split('\n', 2)[0]

		sparseMatrix[counter] = [0 for i in range(totalColumns)]
		for i in range(len(data)):
			location = starts[i] + uniqueValues[i].index(data[i])
			sparseMatrix[counter][location] = 1

		counter += 1

	print "Data read and sparse matrix created"
	print "Use printSomeData() to verify the matrix"
	dataFile.close()


def printSomeData(sparseMatrix, rows):
	for i in range(1, int(rows)):
		data = []
		for j in range(len(sparseMatrix[i])):
			if sparseMatrix[i][j] == 1:
				data.append(sparseMatrix[0][j])

		print data

class ItemSet:
	def __init__(self, candidate):
		self.items = list(candidate)
		self.support = 0
		self.isMaximalFrequent = True
		self.isClosedFrequent = True

	def getItems(self):
		return self.items

	def getSupport(self):
		return self.support

	def getIsMaximalFrequent(self):
		return self.isMaximalFrequent

	def getIsClosedFrequent(self):
		return self.isClosedFrequent

	def setSupport(self, support):
		self.support = support

	def setMaximalFrequent(self, val):
		self.isMaximalFrequent = val

	def setClosedFrequent(self, val):
		self.isClosedFrequent = val

	def canMerge(self, candidate, genParameter):
		if genParameter == 1:
			# corresponds to Fk-1x1 itemset generation method			
			if self.items[len(self.items) - 1] < candidate.getItems()[0]:				
				self.candidate = list(self.items)
				self.candidate.append(candidate.getItems()[0])
				return True
			else:
				return False

		elif genParameter == 2:
			# corresponds to Fk-1XFk-1 itemset generation method
			A = list(self.items)
			B = list(candidate.getItems())
			
			for l in range(len(A) - 1):
				if A[l] != B[l]:
					return False			

			if A[len(A) - 1] == B[len(B) - 1]:
				return False
			else:
				self.candidate = list(A[:len(A) - 1])
				if A[len(A) - 1] < B[len(B) - 1]:
					self.candidate.append(A[len(A) - 1])
					self.candidate.append(B[len(B) - 1])					
				else:
					self.candidate.append(B[len(B) - 1])
					self.candidate.append(A[len(A) - 1])		
			
			return True
		return False

	def merge(self, candidate, genParameter):
		if self.canMerge(candidate, genParameter):
			return ItemSet(list(self.candidate))
		else:
			return None

	def equals(self, candidate):
		if self.items == candidate.getItems():
			return True
		else:
			return False


def countSupport(sparseMatrix, itemSet):
	candidate = itemSet.getItems()
	support = 0
	for i in range(1, len(sparseMatrix)):
		count = 0
		for j in range(len(candidate)):
			if sparseMatrix[i][candidate[j]] == 1:
				count += 1

		if count == len(candidate):
			support += 1

	itemSet.setSupport(support)
	return support

def checkDuplicate(k_ItemSets, candidate):
	if len(candidate.getItems()) in k_ItemSets:
		for item in k_ItemSets[len(candidate.getItems())]:
			if item.equals(candidate):
				return True

	return False

def addCandidate(k_ItemSets, candidate, kValue, parent1, parent2, minSupport):
	global frequentItemSets
	global generatedItemSets

	if candidate != None:
		# print candidate.getItems()
		if not checkDuplicate(k_ItemSets[kValue], candidate):
			generatedItemSets += 1
			support = countSupport(sparseMatrix, candidate)			
			print "Found support of %d for %s candidate against minSupport of %d" % (support, str(candidate.getItems()), minSupport)		
		if support >= minSupport:
			parent1.setMaximalFrequent(False)
			parent2.setMaximalFrequent(False)

			if support == parent1.getSupport():
				parent1.setClosedFrequent(False)
			if support == parent2.getSupport():
				parent2.setClosedFrequent(False)

			k_ItemSets[kValue].append(copy.copy(candidate))
			frequentItemSets += 1

def printK_ItemSet(k_ItemSets):
	for x in k_ItemSets:
		print x.getItems()

def getStatistics(k_ItemSets):
	totalFreqCount = 0
	maximalFreqCount = 0
	closedFreqCount = 0

	for x in k_ItemSets:
		for item in k_ItemSets[x]:
			totalFreqCount += 1			
			if item.getIsMaximalFrequent():
				maximalFreqCount += 1
			
			if item.getIsClosedFrequent():
				closedFreqCount += 1

	print "%d items are frequent" % totalFreqCount
	print "%d items are closed frequent" % closedFreqCount
	print "%d items are maximal frequent" % maximalFreqCount


class Rule:
	def __init__(self, lhs, rhs, confidence):
		self.lhs = lhs
		self.rhs = rhs
		self.confidence = confidence

	def printRule(self, mappingRow):
		ruleString = ""

		for x in self.lhs:
			ruleString += mappingRow[x] + ", "			

		ruleString = ruleString[: len(ruleString) - 2]
		ruleString += " -> "

		for x in self.rhs:
			ruleString += mappingRow[x] + ", "			

		ruleString = ruleString[: len(ruleString) - 2]

		print ruleString

	def getLength(self):
		return len(self.lhs) + len(self.rhs)

def getSubsetSupport(candidate):
	global k_ItemSets

	for item in k_ItemSets[len(candidate)]:		
		if item.getItems() == candidate:			
			return item.getSupport()

	print "Subset not found"
	return 1

def buildRules(lhs, rhs, totalSupport, confidenceCutoff):	
	global rules
	global sparseMatrix

	if len(lhs) > 1:
		for i in range(len(lhs) - 1):
			newlhs = list(lhs)
			newlhs.pop(i)
			newrhs = list(rhs)
			newrhs.append(lhs[i])
			newrhs.sort()
			buildRules(newlhs, newrhs, totalSupport, confidenceCutoff)	

	if len(rhs) > 0:		
		confidence = (float(totalSupport) / getSubsetSupport(lhs))		
		print "Considering %s -> %s with confidence %.2f against cutoff of %.2f" % (lhs, rhs, confidence, confidenceCutoff)
		if confidence >= confidenceCutoff:
			rule = Rule(lhs, rhs, confidence)		

			if rule.getLength() not in rules:
				rules[rule.getLength()] = []

			rules[rule.getLength()].append(rule)

def printRules():
	global rules
	global sparseMatrix

	print "\nHere are the mined rules"
	print "-" * 90
	for i in rules:
		for item in rules[i]:
			item.printRule(sparseMatrix[0])
		print "-" * 90
	
def startRuleBuilding():
	global k_ItemSets
	global confidenceCutoff

	for i in k_ItemSets:
		for candidate in k_ItemSets[i]:
			lhs = candidate.getItems()
			rhs = []			
			buildRules(lhs, rhs, candidate.getSupport(), confidenceCutoff)

	printRules()

def generateCandidatesFk_1x1(sparseMatrix, supportThres):
	minSupportCount = math.floor((len(sparseMatrix) - 1) * (float(supportThres) / 100))

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
		item = ItemSet(candidate)		
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
					
					addCandidate(k_ItemSets, candidate, i, j, k, minSupportCount)
					
			# printK_ItemSet(k_ItemSets[i])
			print "%d-frequent k_ItemSets generated" % i

	print "%s item sets were generated" % generatedItemSets	
	print "Method used was Fk-1x1"

	getStatistics(k_ItemSets)

def generateCandidatesFk_1xk_1(sparseMatrix, supportThres):
	minSupportCount = math.floor((len(sparseMatrix) - 1) * (float(supportThres) / 100))
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
		item = ItemSet(candidate)		
		generatedItemSets += 1
		if countSupport(sparseMatrix, item) >= minSupportCount:
			k_ItemSets[1].append(item)
			frequentItemSets += 1

	printK_ItemSet(k_ItemSets[1])

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

					addCandidate(k_ItemSets, candidate, i, k_ItemSets[i - 1][j], k_ItemSets[i - 1][k], minSupportCount)					

			# printK_ItemSet(k_ItemSets[i])
			print "%d-frequent k_ItemSets generated" % i

		for i in range(1, len(sparseMatrix[0])):
			if i in k_ItemSets:
				for x in k_ItemSets[i]:
					print x.getItems()

		print "%s item sets were generated" % generatedItemSets		
		print "Method used was Fk-1xFk-1"

		getStatistics(k_ItemSets)

sparseMatrix = {}
k_ItemSets = {}
rules = {}

generatedItemSets = 0
frequentItemSets = 0
supportThres = float(sys.argv[2])
confidenceCutoff = float(sys.argv[3])

readFile(sys.argv[1], sparseMatrix)

generateCandidatesFk_1xk_1(sparseMatrix, supportThres)
startRuleBuilding()
# printSomeData(sparseMatrix, 20)