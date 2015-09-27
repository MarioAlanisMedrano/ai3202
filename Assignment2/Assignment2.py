#Assignment2
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
				
		for y in (range(0,len(mapMatrix))):
			for x in (range(0,len(mapMatrix[y]))):
				mapMatrix[y][x] = Node(y,x,int(mapMatrix[y][x]))
				#print y,x, " ",mapMatrix[y][x].typeN
		return mapMatrix
	
class Node:
	def __init__(self, x, y, typeN):
		self.x = x
		self.y = y
		self.typeN = typeN #0 = good, 1 == mtn, 2 = wall
		self.cost = 0
		self.p = None
		self.f = 0
		
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
		self.goalx = 0
		self.goaly = len(world[0])-1
		self.world = world
		self.start = world[len(world)-1][0]
		if htype == 1:
			self.htype = self.calcManhattan
		else:
			self.htype = self.calcother
		
	def calcManhattan(self,x,y):
		return abs(x - self.goalx) + abs(y - self.goaly)
		
	def calcother(self,x,y):
		return math.sqrt((x-self.goalx)**2 + (y-self.goaly)**2)
	
	def getAdj(self, baseN):
		adjl = []
		for x in range(baseN.x - 1, baseN.x + 2):
			for y in range(baseN.y - 1, baseN.y + 2):
				if(x >= 0 and x < len(self.world) and y >= 0 and y < len(self.world[x]) and not(x == baseN.x and y == baseN.y)):
					if (self.world[x][y].typeN != 2):
						adjN = self.world[x][y]
						adjl.append(adjN)
		return adjl
	
	def Astar(self):
		#open and closed lists defined in the class initializer
		locationseval = 0
		#self.Openl.append(self.start)
		self.Openl[self.start] = self.start.f
		while self.Openl != {}:
			#finds node with smallest cost
			min_val = min(self.Openl, key=self.Openl.get)
			locationseval = locationseval +1
			for val in self.Openl:
				if (self.Openl[val] == min_val):
					node = val
					print "node with min is at"
					print node.x, node.y
					break
			print "removing node: XXXXXXXX"
			print node.x, node.y
			del self.Openl[node]
			
			if (node.x != self.goalx and node.y != self.goaly):
				print "not found it yet"
				print node.x, node.y
				self.Closedl[node] = node.f
				node_adj = self.getAdj(node)
				for n in node_adj:
					#print "looking at adj"
					#print n.x, n.y
					if (n.typeN != 2 and not(n in self.Closedl)):
						n.setparent(node,self.htype)#calculates n.f
						if (n in self.Openl):
							#print "n is in open"
							#print node.f + calcCost(n,node)
							#replace if f(n) is lower than n.f
							if (n.f > (node.f + calcCost(n,node))):
								n.f = node.f + calcCost(n,node)
						else:
							self.Openl[n] = n.f
			else:
				print "found it"
				break
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX	


astar = WorldAstar(getMap(),1)

astar.Astar()
