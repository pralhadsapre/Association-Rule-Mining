import math
import copy

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