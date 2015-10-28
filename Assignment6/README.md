#Implementation of Bayes Nets#

TO RUN CODE: python assingment6.py -pS=0.4 -g"c|s"

Note that my code doesn't parse strings, must have quotes around expresion in order to work

Here the different flags run different probabilities
-g conditional progrability
-j joint probability
-m marginal probability
-p sets the probability of Pollution or Smoking

Each letter used represents a different node (see writeup for image)
p = pollution, either "L" low or "H" high
s = smoked, either "T" true, or "F" false
c = cancer, c is cancer, ~c is not cancer
d = has dyspnoea (trouble breathing), d is dyspnoea, ~d is not dyspnoea
x = x-ray is possitive for cancer, x is possitive, ~x is negative

Use capital letter to express that you want the probability distribution for the variable

This runs only the calculations in the given table, some joint probabilities as given in the write up, and all the marginal probability distribution. Most of this code is hard coded. Din't really have time to impliment this code inteligently.
