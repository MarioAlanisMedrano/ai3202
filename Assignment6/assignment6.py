#Assignment 6
#Bayes Nets

import getopt, sys, re

#capital leter: return the probability distribution for the variable
#lower case: is reserved for the name of the varibles

class Node:
	def __init__(self, name):
		self.name = name
		self.conditionals = {}
		self.prob = {}
		
	def set_prob(self, key, value):
		self.prob[key] = value
		
	def __str__(self):
		return (str(self.name))
	
def setNodes(p_val, s_val):
	#initializes values for nodes, returns an array of nodes
	#p = pollution, s = smoker, c = caner, d = dyspnoea, x = x-ray
	#p = high, ~p = low. s|c|d|x = True, ~s|~c|~d|~x = False
	
	nodes = [] #contains nodes of class Node, each node of tree
	
	#smoker
	s = Node("Smoker")
	s.set_prob("T", s_val)
	s.set_prob("F", (1-s_val))
	nodes.append(s)
	#pollution
	p = Node("Pollution")
	p.set_prob("L", p_val)
	p.set_prob("H", (1-p_val))
	nodes.append(p)
	#cancer
	c = Node("Cancer")
	c.set_prob("~ps", .05) #high p, s
	c.set_prob("~p~s", .02) #high p, ~s
	c.set_prob("ps", .03) #low p, s
	c.set_prob("p~s", .001) #low p, ~s
	nodes.append(c)
	#xray
	x = Node("X-ray")
	x.set_prob("c", .9)
	x.set_prob("~c", .2)
	nodes.append(x)
	#Dyspnoea
	d = Node("Dyspnoea")
	d.set_prob("c", .65)
	d.set_prob("~c",.3)
	nodes.append(d)
	
	return nodes

list_prob = {} #all probabilities will be stored here

'''
Marginal Probabilities
the calculations go here
prob of node given parents (node,parent(s))
'''

def mar_c(c, p, s):
	prob = c.prob["~ps"]*p.prob["H"]*s.prob["T"]
	prob += c.prob["~p~s"]*p.prob["H"]*s.prob["F"]
	prob += c.prob["ps"]*p.prob["L"]*s.prob["T"]
	prob += c.prob["p~s"]*p.prob["L"]*s.prob["F"]
	
	list_prob["mar_c"] = prob
	list_prob["~mar_c"] = (1-prob)
	return prob

def mar_x(x,c):
	prob = x.prob["c"]*list_prob["mar_c"]
	prob += x.prob["~c"]*list_prob["~mar_c"]
	
	list_prob["x"] = prob
	list_prob["~x"] = (1-prob)
	return prob

def mar_d(d,c):
	prob = d.prob["c"]*list_prob["mar_c"]
	prob += d.prob["~c"]*list_prob["~mar_c"]
	
	list_prob["d"] = prob
	list_prob["~d"] = (1-prob)
	return prob

#END OF MARGINALS

'''
Conditionals Probabilities
the calculations go here
P(A|B) = [P(B|A)*P(A)]/P(B)
'''

def c_given_p_l(c, p, s):
	numerator = c.prob["ps"]*p.prob["L"]*s.prob["T"]
	numerator += c.prob["p~s"]*p.prob["L"]*s.prob["F"]
	prob = numerator/p.prob["L"]
	
	list_prob["c_given_p_l"] = prob
	return prob
	
def c_given_p_h(c, p, s):
	numerator = c.prob["~ps"]*p.prob["H"]*s.prob["T"]
	numerator += c.prob["~p~s"]*p.prob["H"]*s.prob["F"]
	prob = numerator/p.prob["H"]
	
	list_prob["c_given_p_h"] = prob
	return prob
	
def c_given_s(c, p, s):
	numerator = c.prob["ps"]*p.prob["L"]*s.prob["T"]
	numerator += c.prob["~ps"]*p.prob["H"]*s.prob["T"]
	prob = numerator/s.prob["T"]
	
	list_prob["c_given_s"] = prob
	return prob
	
def p_h_given_d(d, p, s, c):
	numerator = d_given_p_h(d, p, s, c)*p.prob["H"]
	prob = numerator/list_prob["d"]
	
	list_prob["p_h_given_d"] = prob
	return prob

def d_given_p_h(d, p, s, c):
	numerator = d.prob["c"]*c.prob["~ps"]*p.prob["H"]*s.prob["T"]
	numerator += d.prob["c"]*c.prob["~p~s"]*p.prob["H"]*s.prob["F"]
	numerator += d.prob["~c"]*(1-c.prob["~ps"])*p.prob["H"]*s.prob["T"]
	numerator += d.prob["~c"]*(1-c.prob["~p~s"])*p.prob["H"]*s.prob["F"]
	denominator = c.prob["~ps"]*p.prob["H"]*s.prob["T"]
	denominator += c.prob["~p~s"]*p.prob["H"]*s.prob["F"]
	denominator += (1-c.prob["~ps"])*p.prob["H"]*s.prob["T"]
	denominator += (1-c.prob["~p~s"])*p.prob["H"]*s.prob["F"]
	prob = numerator/denominator
	
	list_prob["d_given_p_h"] = prob
	return prob

def s_given_d(d, p, s, c):
	numerator = d_given_s(d, p, s, c)*s.prob["T"]
	prob = numerator/list_prob["d"]
	
	list_prob["s_given_p_h"] = prob
	return prob	
	
def d_given_s(d, p, s, c):
	numerator = d.prob["c"]*c.prob["ps"]*p.prob["L"]*s.prob["T"]
	numerator += d.prob["c"]*c.prob["~ps"]*p.prob["H"]*s.prob["T"]
	numerator += d.prob["~c"]*(1-c.prob["ps"])*p.prob["L"]*s.prob["T"]
	numerator += d.prob["~c"]*(1-c.prob["~ps"])*p.prob["H"]*s.prob["T"]
	denominator = c.prob["ps"]*p.prob["L"]*s.prob["T"]
	denominator += c.prob["~ps"]*p.prob["H"]*s.prob["T"]
	denominator += (1-c.prob["ps"])*p.prob["L"]*s.prob["T"]
	denominator += (1-c.prob["~ps"])*p.prob["H"]*s.prob["T"]
	prob = numerator/denominator
	
	list_prob["d_given_s"] = prob
	return prob
	
def c_given_d(d, c):
	prob = (d.prob["c"]*list_prob["mar_c"])/list_prob["d"]
	list_prob["c_given_d"] = prob
	return prob
	
def x_given_d(x, d, c):
	numerator = x.prob["c"]*list_prob["mar_c"]*d.prob["c"]
	numerator += x.prob["~c"]*list_prob["~mar_c"]*d.prob["~c"]
	prob = numerator/list_prob["d"]
	
	list_prob["x_given_d"] = prob
	return prob

def x_given_s(x, c, p, s):
	numerator = x.prob["c"]*c.prob["ps"]*s.prob["T"]*p.prob["L"]
	numerator += x.prob["c"]*c.prob["~ps"]*s.prob["T"]*p.prob["H"]
	numerator += x.prob["~c"]*(1-c.prob["ps"])*s.prob["T"]*p.prob["L"]
	numerator += x.prob["~c"]*(1-c.prob["~ps"])*s.prob["T"]*p.prob["H"]
	denominator = c.prob["ps"]*s.prob["T"]*p.prob["L"]
	denominator += c.prob["~ps"]*s.prob["T"]*p.prob["H"]
	denominator += (1-c.prob["ps"])*s.prob["T"]*p.prob["L"]
	denominator += (1-c.prob["~ps"])*s.prob["T"]*p.prob["H"]
	prob = numerator/denominator
	
	list_prob["x_given_s"] = prob
	return prob

def p_h_given_c(c, p, s):
	numerator = c_given_p_h(c, p, s)*p.prob["H"]
	prob = numerator/list_prob["mar_c"]
	
	list_prob["p_h_given_c"] = prob
	return prob
	
def s_given_c(c, p, s):
	numerator = c_given_s(c, p, s)*s.prob["T"]
	prob = numerator/list_prob["mar_c"]
	
	list_prob["s_given_c"] = prob
	return prob

def d_given_c(d, c, p, s):
	numerator = c_given_d(d, c)*list_prob["d"]
	prob = numerator/list_prob["mar_c"]
	
	list_prob["d_given_c"] = prob
	return prob

def p_h_given_c_s(c, s, p):
	numerator = c.prob["~ps"]*s.prob["T"]*p.prob["H"]
	denominator = c.prob["~ps"]*s.prob["T"]*p.prob["H"]
	denominator += c.prob["ps"]*s.prob["T"]*p.prob["L"]
	prob = numerator/denominator
	
	list_prob["p_h_given_c_s"] = prob
	return prob

def p_h_given_d_s(p, s, c, d):
	numerator = d.prob["c"]*c.prob["~ps"]*p.prob["H"]*s.prob["T"]
	numerator += d.prob["~c"]*(1-c.prob["~ps"])*p.prob["H"]*s.prob["T"]
	denominator = d.prob["c"]*c.prob["~ps"]*p.prob["H"]*s.prob["T"]
	denominator += d.prob["c"]*c.prob["ps"]*p.prob["L"]*s.prob["T"]
	denominator += d.prob["~c"]*(1-c.prob["~ps"])*p.prob["H"]*s.prob["T"]
	denominator += d.prob["~c"]*(1-c.prob["ps"])*p.prob["L"]*s.prob["T"]
	prob = numerator/denominator
	
	list_prob["p_h_given_d_s"] = prob
	return prob
	
	
#END OF CONDITIONALS

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:],"g:j:m:p:")
	except getopt.GetoptError as err:
		print str(err) #prints error
		sys.exit(2)
	flag = None #this is just the flag
	f_input = None #this is just a
	p_val = .9 #default
	s_val = .3 #default
	nodes = setNodes(p_val,s_val)
	for o, a in opts:
		if o == "-g": 
			#conditinal probability
			flag = o
			f_in = a
		elif o in ("-j"): 
			#joint probability
			flag = o
			f_in = a
		elif o in ("-m"): 
			#marginal probability
			flag = o
			f_in = a
		elif o in ("-p"): #
			#set prior for p or s
			#this code gets the first number after the "P", no spaces please
			probIN = float(re.findall(".\d+",a[1:])[0])
			if a[0] == "S":
				nodes = setNodes(p_val,probIN)
			elif a[0] == "P":
				nodes = setNodes(probIN,s_val)
		else:
			assert False, "unhandled option"
	
	#set var names
	s = nodes[0]
	p = nodes[1]
	c = nodes[2]
	x = nodes[3]
	d = nodes[4]
	print('prob s::',s.prob["T"])
	print('prob p::',p.prob["L"])
	
	#calculate marginal probabilities
	mar_c(c,p,s)
	mar_x(x,c)
	mar_d(d,c)
	#now run the correct flag
	if flag == "-m": #marginal
		if f_in == "p":
			print(p.prob["L"])
		elif f_in == "~p":
			print(p.prob["H"])
		elif f_in == "s":
			print(s.prob["T"])
		elif f_in == "~s":
			print(s.prob["F"])
		elif f_in == "c":
			print(list_prob["mar_c"])
		elif f_in == "~c":
			print(list_prob["~mar_c"])
		elif f_in == "x":
			print(list_prob["mar_x"])
		elif f_in == "~x":
			print(list_prob["~mar_x"])
		elif f_in == "d":
			print(list_prob["mar_d"])
		elif f_in == "~d":
			print(list_prob["~mar_d"])
		else:
			print("Not a valid -m option")
			sys.exit(2)
	if flag == "-g": #conditional
		if f_in == "c|p": #dn
			print(c_given_p_l(c, p, s))
		elif f_in == "c|~p": #dn
			print(c_given_p_h(c, p, s))
		elif f_in == "c|s": #dn
			print(c_given_s(c, p, s))
			
		elif f_in == "~p|d":
			print(p_h_given_d(d, p, s, c))
		elif f_in == "s|d":
			print(s_given_d(d, p, s, c))
		elif f_in == "c|d":
			print(c_given_d(d, c))
		elif f_in == "x|d":
			print(x_given_d(x, d, c))
		elif f_in  == "d|d":
			print(1)
			
		elif f_in == "~p|s":
			print(p.prob["H"])
		elif f_in == "s|s":
			print(1)
		elif f_in == "c|s":
			print(c_given_s(c, p, s))
		elif f_in == "x|s":
			print(x_given_s(x, c, p, s))
		elif f_in == "d|s":
			print(d_given_s(d, p, s, c))
			
		elif f_in == "~p|c":
			print(p_h_given_c(c, p, s))
		elif f_in == "s|c":
			print(s_given_c(c, p, s))
		elif f_in == "c|c":
			print(1)
		elif f_in == "x|c":
			print(x.prob["c"])
		elif f_in == "d|c":
			print(d_given_c(d, c, p, s))
			
		elif f_in == "~p|cs" or f_in == "~p|sc":
			print(p_h_given_c_s(c, s, p))
		elif f_in == "s|cs" or f_in == "s|sc":
			print(1)
		elif f_in == "c|cs" or f_in == "c|sc":
			print(1)
		elif f_in == "x|cs" or f_in == "x|sc":
			print(x.prob["c"])
		elif f_in == "d|cs" or f_in == "d|sc":
			print(d_given_c(d, c, p, s))
		
		elif f_in == "~p|ds" or f_in == "~p|sd":
			print(p_h_given_d_s(p, s, c, d))
		
if __name__ == "__main__":
	main()
