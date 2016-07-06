import sys

def readFile(fileName):	
	
	sparseMatrix = {}
	
	dataFile = open(fileName, 'r')
	outputFile = open(fileName.split('.')[0] + '_binned.txt', 'w')	

	for line in dataFile:
		data = line.split(',')		
		data[len(data) - 1] = data[len(data) - 1].split('\n', 2)[0]						

		data[0] = str((int(data[0]) / 10) * 10)

		outputString = ''
		for ele in data:
			outputString += ele + ','
		outputString = outputString[:len(outputString) - 1]
		outputString += '\n'

		outputFile.write(outputString)

	dataFile.close()
	outputFile.close()

readFile(sys.argv[1])