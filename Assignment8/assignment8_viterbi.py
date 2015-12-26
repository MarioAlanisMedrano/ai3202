#Assignment 8, completed with Viterbi
#worked with Brooke Robinson and Jennifer Michael
#References: https://en.wikipedia.org/wiki/Viterbi_algorithm

from string import ascii_lowercase #just gets the alphabet in lower case
import math

class LetterN:
	
	def __init__(self, name):
		self.name = name
		self.count = 0.0
		self.initialstate = 0

		self.evidenceDict = {} #evidenceDict['a'] = 7, number of times a was seen in current state
		self.nextevidenceDict = {} #just stores next evidence
		self.probEDict = {} #probEDict['a'] = 0.47, prob of seeing a in the current state
		self.probTDict = {} #transition prob, P(Xt+1 | Xts)
		
def calcEmmision(file):
	allnodes = []
	Eprob = {}

	alphabetWspace = ['_'] #adds a space to correctly calculate everything
	for x in ascii_lowercase:
		alphabetWspace.append(x)

	for letter in alphabetWspace:
		curLetterN = LetterN(str(letter))
		allnodes.append(curLetterN)
		#reads each line of the file and constructs an evidence count
		with open("typos20.data", "r") as myFile:
			for line in myFile:
				x = 0
				e = 2
				if line[x] == letter: #does x[s] == letter in alphabet we are at
					curLetterN.count += 1.0
					# e[s] == x[s]
					if line[e] in curLetterN.evidenceDict:
						curLetterN.evidenceDict[line[e]] += 1 #add to counter
					else:
						curLetterN.evidenceDict[line[e]] = 1 #create entry
		Eprob[letter] = {}
		for letter1 in alphabetWspace:
			if letter1 not in curLetterN.evidenceDict.keys():
				curLetterN.evidenceDict[letter1] = 0.5
		#deniminator = count of the current letter  + number of letters observed when X = a
		#adds 2 due to smoothing method, Laplace smoothing
		file.write("\n")
		denominator = float(curLetterN.count + len(curLetterN.evidenceDict.keys())+2.0)

		for key in sorted(curLetterN.evidenceDict):
			prob = (float(curLetterN.evidenceDict[key]) + 1.0)/denominator
			Eprob[letter][key] = math.log10(prob) #using logs in vertebi algo, saves run time
			curLetterN.probEDict[key] = prob
			file.write("P( {0} | {1} ) = {2} \n".format(key, curLetterN.name ,round(curLetterN.probEDict[key],6)))
	file.write("\n")
	return(allnodes,Eprob)

def calcTransition(allnodes,file):
	Tprob = {}

	alphabetWspace = ['_'] #adds a space to correctly calculate everything
	for x in ascii_lowercase:
		alphabetWspace.append(x)

	for node in allnodes:
		curLetterN = node
		with open("typos20.data", "r") as myFile:
			iterFile = iter(myFile) #used to traverse through the file
			for line in iterFile:
	 			x = 0
				if line[x] == curLetterN.name:
					nextline = next(iterFile,None)
					if (nextline == None):
						break #we are at the end of the file
					else:
						if (nextline[x] in curLetterN.nextevidenceDict):
							curLetterN.nextevidenceDict[nextline[x]] += 1 #add to counter
						else:
							curLetterN.nextevidenceDict[nextline[x]] = 1 #create entry
		Tprob[curLetterN.name] = {}

		#set the rest if the probabilities to zero
		for letter in alphabetWspace:
			if letter not in curLetterN.nextevidenceDict.keys():
				curLetterN.nextevidenceDict[letter] = 0

		#deniminator = count of the current letter  + number of letters observed when X = a
		#adds 2 due to smoothing method, Laplace smoothing
		file.write("\n")
		denominator = float(curLetterN.count + len(curLetterN.nextevidenceDict.keys())+2.0)

		for key in sorted(curLetterN.nextevidenceDict):
			prob = (float(curLetterN.nextevidenceDict[key]) + 1.0)/denominator
			Tprob[curLetterN.name][key] = math.log10(prob) #using logs in vertebi algo, saves run time
			curLetterN.probTDict[key] = prob
			file.write("P( {0} | {1} ) = {2}\n".format(key, curLetterN.name ,round(curLetterN.probTDict[key],6)))
	file.write("\n")
	return Tprob

def calcMarginalInitial(allnodes,file):
	linestotal = 0
	Mprob = {}
	with open("typos20.data", "r") as myFile:
		for line in myFile:
			if line[0] != "_":
				linestotal += 1
	for node in allnodes:
		node.initialstate = float(node.count+1)/float(linestotal+2)
		Mprob[node.name] = math.log10(node.initialstate)
		file.write("P({0}) =  {1}\n".format(node.name, round(node.initialstate,6)))
	return(Mprob)

def Viterbi(Eprob, Tprob, Mprob,file):
	V = [{}] #contains probability at each state
	path = {} #most likely path
	obs = [] #observations
	correct = [] #used to calculate error percent
	with open('typos20Test.data','r') as myFile:
		myFile.readline()
		firstL = myFile.readline()
		for line in myFile:
			obs.append(line[2])
			correct.append(line[0])

	states = ['_'] #adds a space to correctly calculate everything
	for x in ascii_lowercase:
		states.append(x)

	for y in states:
		V[0][y] = Mprob[y] + Eprob[y][firstL[0]]
		path[y] = y

	#run viterbi for t > 0
	for t in range(1,len(obs)):
		V.append({})
		newpath = {}

		for y in states:
			(prob,state) = max((V[t-1][y0] +  Tprob[y0][y] + Eprob[y][obs[t]],y0) for y0 in states)
			V[t][y] = prob
			newpath[y] = path[state] + y

		path = newpath

	n = len(obs) - 1
	(prob, state) = max((V[n][y],y) for y in states)
	print (path[state])
	file.write(path[state])
	file.write("\n")
	file.write("\n")

	#calculates percent error
	count = 0
	pathstate = path[state]
	for i in range(0,len(correct)):
		if correct[i] == pathstate[i]:
			count += 1
	print("Error: " + str((1-count*1.0/len(correct))*100) + "%")
	file.write("Error: " + str((1-count*1.0/len(correct))*100) + "%")

def main():
	file = open("probabilitiesTables.txt","w")
	file.write("**********  emmision probabilities  **********\n")
	file.write("P(Et | Xt)\n")
	allnodes, Eprob = calcEmmision(file)
	#testing dic structure
	# for x in Eprob:
	# 	print(x)
	# 	for y in Eprob[x]:
	# 		print(y,':',Eprob[x][y])
	# print("**********  transition probabilities  **********")
	file.write("************************************************\n")
	file.write("**********  transition probabilities  **********\n")
	file.write("************************************************\n")
	file.write("P(Xt+1 | Xt)\n")
	Tprob = calcTransition(allnodes,file)
	#testing dic structure
	# for x in Tprob:
	# 	print(x)
	# 	for y in Tprob[x]:
	# 		print(y,':',Tprob[x][y])
	# print("**********  marginal.initial probabilities  **********\n")
	file.write("**********  marginal/initial probabilities  **********\n")
	Mprob = calcMarginalInitial(allnodes,file)
	file.close()
	file = open("StateSequence.txt","w")
	Viterbi(Eprob, Tprob, Mprob,file)
	file.close()

if __name__ == '__main__':
	main()