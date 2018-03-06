#!/usr/bin/python

import math as m
sum = 0
linecount = 0

 

for line in open("./temp", 'r'):
  tokens = line.split()
  sent_prob = float(tokens[1])
  sum -= m.log(sent_prob,2)
  linecount += 1

 

print("Cross entropy = ", sum / linecount)
