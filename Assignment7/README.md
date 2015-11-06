#Samping Probability#

PRIOR SAMPLING

('P(c = true)', 0.48)

('P(c = true | r = true)', 0.8869565217391304)

('P(s = true | w = true)', 0.6192644981880687)

('P(s = true | c = true, w = true)', 0.030582030336000002)


EXACT VALUES

('P(c = true)', 0.5)

('P(c = true | r = true)', 0.8)

('P(s = true | w = true)', 0.4736842105263157)

('P(s = true | c = true, w = true)', 0.03804347826086956)



REJECTION SAMPLING

('P(c = true) : ', 0.48)

('P(c = true | r = true)', 0.7333333333333333)

('P(s = true | w = true)', 0.45)

('P(s = true | c = true, w = true)', 0.0)

4.   No. Calculating P(c) for both prior and rejection is quite accurate. The prior P(c|r) is a bit on the high side,
this is due to not rejecting samples and just counting everything. The rejection P(c|r) is far more accurate due
to rejecting samples that don't fit the model, and also to be honed probably less rounding errors due to the simpler
calculation used for rejection. Same store applied to the P(s|w) in prior and rejection. Now the prior sampling was
very accurate on the case of P(s|cw), which honestly baffles me since the probability is so low it shouldn't really
show up in the prior sampling. The rejection P(s|cw) is zero, which seems correct to me since we are rejecting a lot 
more samples. And due to the low proability of this occurrace, it makes sense for rejectiont to not get any samples.
