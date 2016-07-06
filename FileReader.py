def readFile(fileName, columns):	
	
	sparseMatrix = {}
	
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
				uniqueValues[x].append(data[x])

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

		sparseMatrix[counter] = [False for i in range(totalColumns)]
		for i in range(len(data)):
			location = starts[i] + uniqueValues[i].index(data[i])
			sparseMatrix[counter][location] = True

		counter += 1

	print "Data read and sparse matrix created"
	print "Use printSomeData() to verify the matrix"
	dataFile.close()

	return sparseMatrix

def printSomeData(sparseMatrix, rows):
	for i in range(1, int(rows)):
		data = []
		for j in range(len(sparseMatrix[i])):
			if sparseMatrix[i][j] == 1:
				data.append(sparseMatrix[0][j])

		print data