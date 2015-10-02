#THIS IS THE EXPERIMENTAL
#Assignment2
#Worked with Brooke Robinson
import sys
import math


def calcCost(n1,n2):
	return 10 + int(n1.x != n2.x and n1.y != n2.y)*4 + n2.typeN*10	

def getMap():
	with open(sys.argv[1], 'r') as f:
		mapMatrix = []
		for line in f:
			line = line.strip()
			if len(line) > 0:
				mapMatrix.append(map(int, line.split()))
		#print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in mapMatrix]))
		for x in (range(0,len(mapMatrix))):
			for y in (range(0,len(mapMatrix[x]))):
				mapMatrix[x][y] = Node(x,y,int(mapMatrix[x][y]))
				#print x,y, " ",mapMatrix[x][y].typeN
		return mapMatrix
	
class Node:
	def __init__(self, x, y, typeN):
		self.x = x
		self.y = y
		self.typeN = typeN #0 = good, 1 == mtn, 2 = wall, 3 = snake, 4 = barn
		if typeN == 1:
			self.reward = -1.0
		elif typeN == 3:
			self.reward = -2.0
		elif typeN == 4:
			self.reward = 1.0
		elif typeN == 50:
			self.reward = 50.0
		else:
			self.reward = 0.0
		self.p = None
		self.uti = 0
		
	def setparent(self, parent):
		self.p = parent
		
class WorldAstar:
	#the map starts at the bottom left
	#where the horse starts is (0,0)
	def __init__(self,world):
		self.Openl = {}
		self.Closedl = {}
		self.goal = world[0][len(world[0])-1]
		self.world = world
		self.start = world[len(world)-1][0]
		self.htype = self.calcManhattan
		self.utiDIC = {}

			
	def calcUti(self, epsilon):
		sigma = 0.0
		while (sigma < (epsilon*(1.0-0.9)/0.9)):
			sigma = 0.0
			for i in (range(0,len(self.world))):
				for node in self.world[i]:
					maxnum = self.calcMaxOption(node)
					utiprime = node.reward + 0.9*maxnum
					#print node.x,node.y
					if not(node in self.utiDIC):
						self.utiDIC[node] = 0
						#print self.utiDIC[node]
					if abs(utiprime - self.utiDIC[node]) > sigma:
						sigma = abs(utiprime - self.utiDIC[node])
					self.utiDIC[node] = utiprime
					if node.typeN == 2:
						self.utiDIC[node] = 0
					node.uti = self.utiDIC[node]
		#print('\n'.join(['	'.join(['{0:.2f}'.format(item.uti) for item in row]) for row in self.world]))
	
	def calcMaxOption(self, node):
		adjlist = self.getAdj(node)
		listofvalues = []
		for tempnode in adjlist:
			if tempnode.x == node.x:
				#look at changing y values for left and right rewards
				if (tempnode.y >= 0 and tempnode.y < len(self.world[0])-1):
					if ((self.world[tempnode.x][tempnode.y+1]) in adjlist):
						nodelook1 = self.world[node.x][node.y+1]
					else:
						nodelook1 = 0.0
					if (self.world[node.x][node.y-1] in adjlist):
						nodelook2 = self.world[node.x][node.y-1]
					else:
						nodelook2 = 0.0
					if (nodelook1 == 0.0) and (nodelook2 == 0.0):
						listofvalues.append(0.8*(tempnode.reward) + 0.1*(nodelook1) + 0.1*(nodelook2))
					elif nodelook1 == 0.0:
						listofvalues.append(0.8*(tempnode.reward) + 0.1*(nodelook1) + 0.1*(nodelook2.reward))
					elif nodelook2 == 0.0:
						listofvalues.append(0.8*(tempnode.reward) + 0.1*(nodelook1.reward) + 0.1*(nodelook2))
					else:
						listofvalues.append(0.8*(tempnode.reward) + 0.1*(nodelook1.reward) + 0.1*(nodelook2.reward))
			elif tempnode.y == node.y:
				#look at changing x values for left and right rewards
				if (tempnode.x >= 0 and tempnode.x < len(self.world)-1):
					if (self.world[tempnode.x+1][tempnode.y] in adjlist):
						nodelook1 = self.world[node.x+1][node.y]
					else:
						nodelook1 = 0.0
					if (self.world[node.x-1][node.y] in adjlist):
						nodelook2 = self.world[node.x-1][node.y]
					else:
						nodelook2 = 0.0
					if (nodelook1 == 0.0) and (nodelook2 == 0.0):
						listofvalues.append(0.8*(tempnode.reward) + 0.1*(nodelook1) + 0.1*(nodelook2))
					elif nodelook1 == 0.0:
						listofvalues.append(0.8*(tempnode.reward) + 0.1*(nodelook1) + 0.1*(nodelook2.reward))
					elif nodelook2 == 0.0:
						listofvalues.append(0.8*(tempnode.reward) + 0.1*(nodelook1.reward) + 0.1*(nodelook2))
					else:
						listofvalues.append(0.8*(tempnode.reward) + 0.1*(nodelook1.reward) + 0.1*(nodelook2.reward))
		#the loop ran through the entire list of adj nodes, select max values
		return max(listofvalues)
	
	def calcManhattan(self,x,y):
		return abs(x - self.goal.x) + abs(y - self.goal.y)
	
	def getAdj(self, baseN):
		adjl = []
		for x in range(baseN.x - 1, baseN.x + 2):
			for y in range(baseN.y - 1, baseN.y + 2):
				if(x >= 0 and x < len(self.world) and y >= 0 and y < len(self.world[x]) and not(x == baseN.x and y == baseN.y)):
					if not(x == baseN.x-1 and y == baseN.y-1) and not(x == baseN.x+1 and y == baseN.y+1) and not(x == baseN.x-1 and y == baseN.y+1) and not(x == baseN.x+1 and y == baseN.y-1):
						#the above if statement gets rids of the corners: downleft, uprigth, upleft, downright
						if (self.world[x][y].typeN != 2):
							adjN = self.world[x][y]
							adjl.append(adjN)
		return adjl
	
	def getPath(self,node):
		print "Path taken:"
		stringArray = []
		while not(node.x == self.start.x and node.y == self.start.y):
			stringArray.append(["(",node.x,",",node.y,")","Utility :",self.utiDIC[node]])
			node = node.p
		stringArray.append(["(",node.x,",",node.y,")","Utility :",self.utiDIC[node]])
		for nodecoor in reversed(stringArray):
			print nodecoor[0], nodecoor[1], nodecoor[2], nodecoor[3], nodecoor[4], nodecoor[5], nodecoor[6]
			
	def Astar(self):
		#open and closed lists defined in the class initializer
		locationseval = 0
		self.Openl[self.start] = self.utiDIC[self.start]
		while self.Openl != {}:
			#finds node with the biggest utility
			max_val_loc = max(self.Openl, key=self.Openl.get)
			max_val = self.Openl[max_val_loc]
			locationseval = locationseval +1
			for val in self.Openl:
				if (self.Openl[val] == max_val):
					node = val
					break
			del self.Openl[node]
			if (node.x == self.goal.x and node.y == self.goal.y):
				self.getPath(node)
				break
			self.Closedl[node] = node.uti
			node_adj = self.getAdj(node)
			for n in node_adj:
				if (n.typeN != 2 and not(n in self.Closedl)):
					if not(n in self.Openl) or (n.uti > node.uti):
						n.setparent(node)
						if not(n in self.Openl):
							self.Openl[n] = n.uti
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX	

astar = WorldAstar(getMap())
astar.calcUti(float(sys.argv[2]))
astar.Astar()

#try:
	#astar = WorldAstar(getMap())
	#astar.calcUti(float(sys.argv[2]))
	#astar.Astar()
#except:
	#print "please give world file name and heuristic. Ex: python Assignment5.py World1MDP.txt 0.5"
