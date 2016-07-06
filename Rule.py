class Rule:
	def __init__(self, lhs, rhs, confidence):
		self.lhs = lhs
		self.rhs = rhs
		self.confidence = confidence

	def printRule(self, mappingRow):
		ruleString = ""

		# print str(self.lhs) + " -> " + str(self.rhs)

		for x in self.lhs:
			ruleString += mappingRow[x] + ", "			

		ruleString = ruleString[: len(ruleString) - 2]
		ruleString += " -> "

		for x in self.rhs:
			ruleString += mappingRow[x] + ", "		

		ruleString = ruleString[: len(ruleString) - 2]
		# ruleString += ("\t Interestingness: %.2f" % self.confidence)

		print ruleString

	def getLength(self):
		return len(self.lhs) + len(self.rhs)

	def equals(self, rule):
		if self.lhs == rule.lhs and self.rhs == rule.rhs:
			return True
		else:
			return False