import math
import copy
import Rule as r

def getSubsetSupport(candidate):
	global k_ItemSets

	for item in k_ItemSets[len(candidate)]:		
		if item.getItems() == candidate:			
			return item.getSupport()

	print "Subset not found"
	return 1

def checkDuplicate(rule):
	global rules

	for item in rules[rule.getLength()]:
		if item.equals(rule):
			return True

	return False

def buildRules(lhs, rhs, totalSupport, confidenceCutoff):	
	global rules
	global rulesList

	if len(lhs) > 1:
		for i in reversed(range(0, len(lhs))):
			newlhs = list(lhs)
			newlhs.pop(i)
			newrhs = list(rhs)
			newrhs.append(lhs[i])
			newrhs.sort()
			buildRules(newlhs, newrhs, totalSupport, confidenceCutoff)	

	if len(rhs) > 0:
		if interestingMeasure == 1:
			confidence = (float(totalSupport) / getSubsetSupport(lhs))		
		elif interestingMeasure == 2:
			confidence = (float(totalSupport) / (getSubsetSupport(lhs) * getSubsetSupport(rhs)))

		# print ".",
		# print "Considering %s -> %s with confidence %.10f against cutoff of %.2f" % (lhs, rhs, confidence, confidenceCutoff)
		if confidence >= confidenceCutoff:
			rule = r.Rule(lhs, rhs, confidence)		

			if rule.getLength() not in rules:
				rules[rule.getLength()] = []

			if not checkDuplicate(rule):
				rules[rule.getLength()].append(rule)
				rulesList.append(rule)
			# else:
			# 	print "\nAha a duplicate rule"

def printRules():
	global rulesList
	
	count = 0
	bruteForceCount = 0
	print "\nHere are the mined rules"
	print "-" * 90
	for i in rules:
		for item in rules[i]:
			count += 1
			item.printRule(mapping)
		print "-" * 90

	rulesList.sort(key = lambda x: x.confidence, reverse = True)

	for rule in rulesList[:30]:
		rule.printRule(mapping)

	for i in k_ItemSets:
		for item in k_ItemSets[i]:
			bruteForceCount += (math.pow(2, len(item.getItems())) - 2)

	print "Total rules generated were %d" % count
	print "If you had used brute force it would have been %d" % bruteForceCount

	if interestingMeasure == 1:
		print "Method - Confidence based pruning"
		print "Pruning threshold was %.2f" % confidenceCutoff
	else:
		print "Method - Lift based interestingness measurement"
	
def startRuleBuilding(mappingRow, generatedItemSets):
	global k_ItemSets
	global confidenceCutoff
	global mapping
	global interestingMeasure

	while True:
		val = int(raw_input("Choose your rule interestingness measure\n1. Confidence\n2. Lift\n"))
		if val != 1 and val != 2:
			print "Please don't enter garbage input"
			continue
		else:			
			break

	interestingMeasure = val
	if interestingMeasure == 1:
		confidenceCutoff = float(raw_input("Choose a threshold for confidence (General range is between 0 to 1 - e.g 0.35): "))
	else:
		# confidenceCutoff = float(raw_input("Choose a threshold for lift (General range is 1 and above - e.g 1.5): "))
		confidenceCutoff = 1.0

	k_ItemSets = generatedItemSets
	mapping = list(mappingRow)

	for i in k_ItemSets:
		if i != 1:
			for candidate in k_ItemSets[i]:
				lhs = candidate.getItems()
				rhs = []			
				buildRules(lhs, rhs, candidate.getSupport(), confidenceCutoff)

	printRules()

k_ItemSets = {}
rules = {}
rulesList = []
mapping = []
confidenceCutoff = 0.0

# default for confidence
interestingMeasure = 1