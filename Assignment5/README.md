Implementation of Markov Decision Processes

TO RUN CODE: python Assingment5.py World1MDP.txt epsilon

Here epsilon helps the program converge to a solution, 0 < epsilon < 9.
The program outputs the utility value for the optimal solution in the shape of the maze, and the path taken. The "total utility" is just the sum of the utility of the path, used to answer the question attached to the problem.

I modified my A* code to traverse through the maze with a Markov Decision Problem.

The total utility is just the utility at each node added up, this is just to easily notice any changes in the solution. The path never changed for all the values I tried. The code just returned 0.0 for all utility when epsilon = 10.0. Any number higher than 10 seems to just return zeros.

I tried the values of epsilon in a reasonable range that works, starting at a value close to 0 but greater. Then I tested random values between 0 and 1. I tested 1 to see if it would work. Then after it did, i tried 10. I noticed this din't work so I keept decrementing untill I found that 9 is the max epsilon value that works.

Epsilon | comment | total utility
---|---|---
0.0	|code doesn't run							|N/A
0.0001	|no change to solution. larger value for the total utilty		|308.9096
0.1	|no change to solution. slightly larger value for the total utility 	|308.8276
*0.5*	|*original solution*							|*308.538137339*
0.9	|no change to solution. slightly smaller value for the total utility	|308.2917
1.0	|no change to solution. slightly smaller value for the total utility	|308.1784
1.1	|no change to solution. same value as 1.0 for the total utility		|308.2917
1.5	|no change to solution. smaller value for the total utility 		|307.8794
2.0	|no change to solution. smaller value for the total utility 		|307.6899
9.0	|no change to solution. even smaller value for the total utility	|303.1769
9.001	|code doesn't run							|N/A
10.0	|code doesn't run							|N/A
