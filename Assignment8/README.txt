how to run my program:
	python assignment8_viterbi.py

YOU NEED THE FILES: typos20.data and typos20Test.data
The first column is the right text, the third is the text with typos. Spaces are represented with '_'. 
If the output seems weird, it is because my code read the first line and does nothing with it.
This is due to typos20Test.data having ".." in the first line, this is weird. This problem can be fixed 
by commenting line 121.

This will output two files: probabilitiesTables.txt, and StateSequence.txt


probabilitiesTables.txt
Contains all of the probabilities calculated using typos20.data as the obserbation data.
They are separated by a header:
"********** NAME OF PROBABILITY **********"
"FORMATED PROBABILITY EQUATION" example: P(Xt|X+1)

Each different probability inside that type of probability
is separated by a new line for readability.



StateSequence.txt
Contains the most probable string of letters based on the observations, third column of typos20Test.data,
using the probabilities calculated using the data found in probabilitiesTables.txt.
In order to work with the small probabilities I used the base 10 log of the probailities to distinguish very
small number from zero. Notice that in my code, the '_' represents a space, and the string is made of just on
line.

After the string, the file has the Error percentage of the most probable string vs the actual text.



I worked with Brooke Robinson and Jennifer Michael on this.
References: https://en.wikipedia.org/wiki/Viterbi_algorithm