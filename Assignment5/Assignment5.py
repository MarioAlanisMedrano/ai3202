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
		self.cost = 0
		self.p = None
		self.f = 0
		self.uti = 0
		
	def setparent(self, parent, h):
		self.p = parent
		self.cost = parent.cost + 10 + int(self.x != parent.x and self.y != parent.y)*4 + self.typeN*10	
		self.f = self.cost + h(self.x,self.y)
		
class WorldAstar:
	#the map starts at the bottom left
	#where the horse starts is (0,0)
	def __init__(self,world,htype):
		self.Openl = {}
		self.Closedl = {}
		self.goal = world[0][len(world[0])-1]
		self.world = world
		self.start = world[len(world)-1][0]
		if htype == 1:
			self.htype = self.calcManhattan
		else:
			self.htype = self.calcother
			
	def calcUti(self, epsilon):
		sigma = 0.0
		while (sigma < (epsilon*(1.0-0.9)/0.9)):
			sigma = 0.0
			for i in (range(0,len(self.world))):
				for node in self.world[i]:
					#print "node :", node.typeN
					maxnum = self.calcMaxOption(node)
					utiprime = node.reward + 0.9*maxnum
					if abs(utiprime - node.uti) > sigma:
						sigma = abs(utiprime - node.uti)
					node.uti = utiprime
					if node.typeN == 2:
						node.uti = 0
		print('\n'.join(['	'.join(['{0:.2f}'.format(item.uti) for item in row]) for row in self.world]))
	
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
		
	def calcother(self,x,y):
		return math.sqrt((x-self.goal.x)**2 + (y-self.goal.y)**2)
		return math.sqrt((x-self.goal.x)**2 + (y-self.goal.y)**2)
	
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
		cost = 0
		stringArray = []
		while not(node.x == self.start.x and node.y == self.start.y):
			stringArray.append(["(",node.x,",",node.y,")"])
			cost += calcCost(node,node.p)
			node = node.p
		stringArray.append(["(",node.x,",",node.y,")"])
		for nodecoor in reversed(stringArray):
			print nodecoor[0], nodecoor[1], nodecoor[2], nodecoor[3], nodecoor[4]
		print "Total Cost: ", cost
			
	def Astar(self):
		#open and closed lists defined in the class initializer
		locationseval = 0
		self.Openl[self.start] = self.start.f
		while self.Openl != {}:
			#finds node with smallest cost
			min_val_loc = min(self.Openl, key=self.Openl.get)
			min_val = self.Openl[min_val_loc]
			locationseval = locationseval +1
			for val in self.Openl:
				if (self.Openl[val] == min_val):
					node = val
					break
			del self.Openl[node]
			if (node.x == self.goal.x and node.y == self.goal.y):
				self.getPath(node)
				print "locations evaluated: ", locationseval
				break
			self.Closedl[node] = node.f
			node_adj = self.getAdj(node)
			for n in node_adj:
				if (n.typeN != 2 and not(n in self.Closedl)):
					if not(n in self.Openl) or (n.f > (node.f + calcCost(n,node))):
						#replace if f(n) is lower than n.f
						n.f = node.f + calcCost(n,node)
						n.setparent(node,self.htype)
						if not(n in self.Openl):
							self.Openl[n] = n.f
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX	

astar = WorldAstar(getMap(),int(sys.argv[2]))
astar.calcUti(float(sys.argv[3]))
#try:
	#astar = WorldAstar(getMap(),int(sys.argv[2]))
	#astar.calcUti(self, sys.argv[3])
	#astar.Astar()
#except:
	#print "please give world file name and heuristic. Ex: python Assignment2.py World1.txt 1"
