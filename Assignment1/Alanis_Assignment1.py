#Assignment 1
#worked with Brooke Robinson


#Problem 1
#implemet a queue

import Queue

q = Queue.Queue()
test_int = [1,2,3,4,5,6,7,8,9,10]
for i in test_int:
	if isinstance(i, int):
		q.put(i)
	else:
		print ('integers only')
		quit()
while q.qsize() > 0:
	print "dequeued: ",q.get()
########################################################################


#Problem 2
#implement stack class

class mystack:
	def __init__(self,data):
		self.data = data
	def push(self,number):
		self.data.append(number)
	def pop(self):
		self.data.pop()
	def checkSize(self):
		return len(self.data)
#stack test ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
test_int = [1,2,3,4,5,6,7,8,9,10]
x = mystack([])
for i in test_int:
	x.push(i)
for i in test_int:
	print (x.data[x.checkSize()-1])
	x.pop()
########################################################################


#Problem 3
#implementing binary tree class

class node:
	def __init__(self, intkey, left, right, parent):
		self.intkey = intkey
		self.left = left
		self.right = right
		self.parent = parent
		
	def getChildren(self):
		return [self.left, self.right]

class myTree:
	def __init__(self, intkey):
		self.root = node(intkey,None, None, None)
		
	def add(self, value, parentValue):
		#looks for parentValue and add value as a child to the node that 
		#contains parentValue 
		if self.root == None:
			self.root = node(value, None, None, None)
		if self.root.intkey == parentValue:
			if self.root.left == None:
				self.root.left = node(value, None, None, self.root)
				print "Added: ", value, "Parent: ", self.root.intkey
				return
			elif self.root.right == None:
				self.root.right = node(value, None, None, self.root)
				print "Added: ", value, "Parent: ", self.root.intkey
				return
			else:
				print "Parent has two children,  thus node was not added"
				return
		else:
			#start recursive search for node
			for x in self.root.getChildren():
				found = self.findr(value, parentValue, x)
				if found == 1:
					return found
		print "Parent not found"
		return 
	
	def findr(self, value, parentValue, root):
		#recursive part of add
		if root == None:
			return 0
		if root.intkey == parentValue:
			#go left
			if root.left == None:
				root.left = node(value, None, None, root)
				#print "Added: ", value, "Parent: ", root.intkey
				return 1
			#go right
			elif root.right == None:
				root.right = node(value, None, None, root)
				#print "Added: ", value, "Parent: ", root.intkey
				return 1
			else:
				print "Parent has two children,  thus node was not added"
				return 0
		else:
			for x in root.getChildren():
				found = self.findr(value, parentValue, x)
				if found == 1:
					return found
	
	def printTree(self):
		#this prints the tree pre-order traversal
		#meaning, root, left sub-tree, right sub-tree
		if self.root == None:
			return
		print self.root.intkey
		for x in self.root.getChildren():
			self.printTreer(x)
			
	def printTreer(self, parent):
		#recursive part of print, passes in parent node
		if parent == None:
			return
		print parent.intkey
		for x in parent.getChildren():
			self.printTreer(x)
	
	def delete(self, value):
		#deletes nodes if they don't have children
		if self.root == None:
			return 
		if self.root.intkey == value:
			#looking for children
			children = self.root.getChildren()
			if children[0] == None and children[1] == None:
				self.root = None
			else:
				print "Node not deleted, has children."
				return
		else:
			#start recursive search for node
			for x in self.root.getChildren():
				found = self.deleter(value, x)
				if found == 1:
					return found
		print "Node not found"
		return
	
	def deleter(self, value, root):
		#recursive part of delete, passes in parent node
		if root == None:
			return
		if root.intkey == value:
			#looking for children
			children = root.getChildren()
			if children[0] == None and children[1] == None:
				if root.parent.left.intkey == value:
					root.parent.left = None
				elif root.parent.right.intkey == value:
					
					root.parent.right = None
				root = None
				return 1
			else:
				print "Node not deleted, has children."
				return 0
		else:
			for x in root.getChildren():
				found = self.deleter(value, x)
				if found == 1:
					return found
		return
#tree test ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
tree = myTree(5)
tree.add(4,5)
tree.add(6,5)
tree.add(3,6)
tree.add(2,6)
tree.add(7,4)
tree.add(8,4)
tree.add(1,2)
tree.add(9,7)
tree.add(10,8)
tree.printTree()
tree.delete(3)
tree.delete(11)
tree.printTree()
########################################################################

#Problem 4
#implemet a graph


class myGraph:
	def __init__(self):
		self.ver = {}
		
	def addVertex(self, value):
		if value in self.ver:
			print "Vertex already exists"
			return
		else:
			self.ver[value] = []
			return
	
	def addEdge(self, value1, value2):
		if value1 == value2:
			return
		if (value1 in self.ver) and (value2 in self.ver):
			self.ver[value1].append(value2)
			self.ver[value2].append(value1)
		else:
			print "One or more vertices not found"
		return
		
	def findVertex(self, value):
		if value in self.ver:
			print self.ver[value]
		return

g = myGraph()
test_int = [1,2,3,4,5,6,7,8,9,10]
counter = 0
for i in test_int:
	print "adding ", i
	g.addVertex(i)
	counter += 1
#graph test ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
g.addEdge(1,2)
g.addEdge(1,3)
g.addEdge(2,3)
g.addEdge(2,4)
g.addEdge(3,4)
g.addEdge(3,5)
g.addEdge(4,5)
g.addEdge(4,6)
g.addEdge(5,6)
g.addEdge(5,7)
g.addEdge(6,7)
g.addEdge(6,8)
g.addEdge(7,8)
g.addEdge(7,9)
g.addEdge(8,9)
g.addEdge(8,10)
g.addEdge(9,10)
g.addEdge(9,1)
g.addEdge(10,1)
g.addEdge(10,2)
g.findVertex(1)
g.findVertex(4)
g.findVertex(10)
########################################################################
