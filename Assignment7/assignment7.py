#test
#Assignment 7
#probability using sampling

samples = [0.82,	0.56,	0.08,	0.81,	0.34,	0.22,	0.37,	0.99,	0.55,	0.61,	0.31,	0.66,	0.28,	1.0,	0.95,	
0.71,	0.14,	0.1,	1.0,	0.71,	0.1,	0.6,	0.64,	0.73,	0.39,	0.03,	0.99,	1.0,	0.97,	0.54,	0.8,	0.97,	
0.07,	0.69,	0.43,	0.29,	0.61,	0.03,	0.13,	0.14,	0.13,	0.4,	0.94,	0.19, 0.6,	0.68,	0.36,	0.67,	
0.12,	0.38,	0.42,	0.81,	0.0,	0.2,	0.85,	0.01,	0.55,	0.3,	0.3,	0.11,	0.83,	0.96,	0.41,	0.65,	
0.29,	0.4,	0.54,	0.23,	0.74,	0.65,	0.38,	0.41,	0.82,	0.08,	0.39,	0.97,	0.95,	0.01,	0.62,	0.32,	
0.56,	0.68,	0.32,	0.27,	0.77,	0.74,	0.79,	0.11,	0.29,	0.69,	0.99,	0.79,	0.21,	0.2,	0.43,	0.81,	
0.9,	0.0,	0.91,	0.01]

#
#
# PRIOR SAMPLING
print("PRIOR SAMPLING")
#

prob = {}
count = {"c":0.0,"s|c":0.0,"s|~c":0.0,"r|c":0.0,"r|~c":0.0,"w|sr":0.0,"w|s~r":0.0,"w|~sr":0.0,"w|~s~r":0.0}
i = 0
#this way I attemped to not overcount, as per suggested by Brooke
'''
cloudy = False
rain = False
sprinkler = False
while i <= 99:
	#counts every samples in sets of 4
	if samples[i] < 0.5:		#cloudy
		count["c"] += 1.0
		cloudy = True
	if samples[i+2] < 0.1 and cloudy:		#sprinkler | cloudy
		count["s|c"] += 1.0
		sprinkler = True
	if samples[i+2] < 0.5 and not(cloudy):		#sprinkler | ~cloudy
		count["s|~c"] += 1.0
		sprinkler = True
	if samples[i+1] < 0.8 and cloudy:		#rain | cloudy
		count["r|c"] += 1.0
		rain = True
	if samples[i+1] < 0.2 and not(cloudy):		#rain | ~cloudy
		count["r|~c"] += 1.0
		rain = True
	if samples[i+3] < 0.99 and sprinkler and rain:		#wet | sprinkler rain
		count["w|sr"] += 1.0
	if samples[i+3] < 0.9 and sprinkler and not(rain):		#wet | sprinkler ~rain
		count["w|s~r"] += 1.0
	if samples[i+3] < 0.9 and not(sprinkler) and rain:		#wet | ~sprinkler rain
		count["w|~sr"] += 1.0
	if samples[i+3] == 0.0 and not(sprinkler) and not(rain):		#wet | ~sprinkler ~rain
		count["w|~s~r"] += 1.0

	i = i + 4
'''

#this is the original way I was counting the samples, I belive this is right
#'''
while i <= 99:
	#counts every samples in sets of 4
	if samples[i] < 0.5:		#cloudy
		count["c"] += 1.0
	if samples[i+2] < 0.1:		#sprinkler | cloudy
		count["s|c"] += 1.0
	if samples[i+2] < 0.5:		#sprinkler | ~cloudy
		count["s|~c"] += 1.0
	if samples[i+1] < 0.8:		#rain | cloudy
		count["r|c"] += 1.0
	if samples[i+1] < 0.2:		#rain | ~cloudy
		count["r|~c"] += 1.0
	if samples[i+3] < 0.99:		#wet | sprinkler rain
		count["w|sr"] += 1.0
	if samples[i+3] < 0.9:		#wet | sprinkler ~rain
		count["w|s~r"] += 1.0
	if samples[i+3] < 0.9:		#wet | ~sprinkler rain
		count["w|~sr"] += 1.0
	if samples[i+3] == 0.0:		#wet | ~sprinkler ~rain
		count["w|~s~r"] += 1.0

	i = i + 4
#'''

#1a
prob["c"] = count["c"]/25.0
print("P(c = true)", prob["c"])


#1b
num = ((count["r|c"]/25.0)*prob["c"])
den = ((count["r|c"]/25.0)*prob["c"]) + ((count["r|~c"]/25.0)*(1-prob["c"]))
prob["r"] = den

#print(num,den, count["r|c"],count["r|c"]/25.0,count["r|~c"],count["r|~c"]/25.0)
prob["c|r"] = num/den
print("P(c = true | r = true)",prob["c|r"])


#1c
prob["s"] = ((count["s|c"]/25.0)*prob["c"]) + ((count["s|~c"]/25.0)*(1-prob["c"]))
prob["w|s"] = ((count["w|sr"]/25.0)*prob["s"]*prob["r"]) + ((count["w|s~r"]/25.0)*prob["s"]*(1-prob["r"]))

num = (prob["w|s"]*prob["s"])
den = prob["w|s"] + ((count["w|~sr"]/25.0)*(1-prob["s"])*prob["r"]) + ((count["w|~s~r"]/25.0)*(1-prob["s"])*(1-prob["r"]))

prob["s|w"] = num/den
print("P(s = true | w = true)",prob["s|w"])


#1d
#P(s|cw) = P(s,c,w)/P(c,w)
#bellow is P(s,c,w)
num = prob["w|s"]*prob["c"]*(count["s|c"]/25.0)
#bellow is P(w|sr)*P(s|c)*P(r)*P(c)+ P(w|s~r)*P(s|c)*(1-P(r))*P(c)
den = ((count["w|sr"]/25.0)*(count["s|c"]/25.0)*(count["r|c"]/25.0) + (count["w|s~r"]/25.0)*(count["s|c"]/25.0)*(1-(count["r|c"]/25.0)))*prob["c"]
den += ((count["w|~sr"]/25.0)*(1-(count["s|c"]/25.0))*(count["r|c"]/25.0) + (count["w|~s~r"]/25.0)*(1-(count["s|c"]/25.0))*(1-(count["r|c"]/25.0)))*prob["c"]
prob["s|cw"] = num/den
print("P(s = true | c = true, w = true)",prob["s|cw"])

#
#
# REJECTION SAMPLING
print("REJECTION SAMPLING")
#

prob = {}
count = [] #an array of arrays, [c,r,s,w] (bool) inside each index
#check = []
c = 0
while c < 100:
	r = c + 1
	s = c + 2
	w = c + 3

	cloudy = False
	rain = False
	sprinkler = False
	wet = False
	#counts every samples in sets of 4
	if samples[c] < 0.5: #c
		cloudy = True
		if samples[r] < 0.8 and samples[s] < 0.1: #rs | c
			rain = True
			sprinkler = True
			if samples[w] < 0.99: #w | rs
				wet = True
				count.append([cloudy,rain,sprinkler,wet])
			else:
				count.append([cloudy,rain,sprinkler,wet])
		elif samples[r] >= 0.8 and samples[s] < 0.1: #~rs | c
			rain = False
			sprinkler = True
			if samples[w] < 0.9: #w | ~rs
				wet = True
				count.append([cloudy,rain,sprinkler,wet])
			else:
				count.append([cloudy,rain,sprinkler,wet])
		elif samples[r] < 0.8 and samples[s] >= 0.1: #r~s |  c
			rain = True
			sprinkler = False
			if samples[w] < 0.9: #w | r~s
				wet = True
				count.append([cloudy,rain,sprinkler,wet])
			else:
				count.append([cloudy,rain,sprinkler,wet])
		elif samples[r] >= 0.8 and samples[s] >= 0.1: #~r~s | c
			rain = False
			sprinkler = False
			wet = False #no probability of wet | ~r~s
			count.append([cloudy,rain,sprinkler,wet])
	if samples[c] >= 0.5: #~c
		cloudy = False
		if samples[r] < 0.2 and samples[s] < 0.5: #rs | c
			rain = True
			sprinkler = True
			if samples[w] < 0.99: #w | rs
				wet = True
				count.append([cloudy,rain,sprinkler,wet])
			else:
				count.append([cloudy,rain,sprinkler,wet])
		elif samples[r] >= 0.2 and samples[s] < 0.5: #~rs | c
			rain = False
			sprinkler = True
			if samples[w] < 0.9: #w | ~rs
				wet = True
				count.append([cloudy,rain,sprinkler,wet])
			else:
				count.append([cloudy,rain,sprinkler,wet])
		elif samples[r] < 0.2 and samples[s] >= 0.5: #r~s |  c
			rain = True
			sprinkler = False
			if samples[w] < 0.9: #w | r~s
				wet = True
				count.append([cloudy,rain,sprinkler,wet])
			else:
				count.append([cloudy,rain,sprinkler,wet])
		elif samples[r] >= 0.2 and samples[s] >= 0.5: #~r~s | c
			rain = False
			sprinkler = False
			wet = False #no probability of wet | ~r~s
			count.append([cloudy,rain,sprinkler,wet])

	#check.append([samples[c],samples[r],samples[s],samples[w]])
	c = c + 4

'''
x = 0
while x < len(check):
	print(check[x],count[x])
	x = x + 1
'''

#used for if statements
c = 0
r = 1
s = 2
w = 3
#problem 3a
i = 0.0
for x in count:
	if x[c] == True:
		i += 1.0
print("P(c = true) : ",i/25.0)
#problem 3b
i = 0.0
for x in count:
	if x[c] == True and x[r] == True:
		i += 1.0
		#print(x,x[c],x[r],i)
print("P(c = true | r = true)",i/25.0)
#problem 3c
i = 0.0
for x in count:
	if x[s] == True and x[w] == True:
		i += 1.0
		#print(x,x[s],x[w],i)
print("P(s = true | w = true)",i/25.0)
#problem 3d
i = 0.0
for x in count:
	if x[s] == True and x[c] == True and x[w] == True:
		i += 1.0
		#print(x,x[s],x[c],x[w],i)
print("P(s = true | c = true, w = true)",i/25.0)
