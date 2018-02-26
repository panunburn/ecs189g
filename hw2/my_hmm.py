#!/usr/bin/python

# David Bamman
# 2/14/14
#
# Python port of train_hmm.pl:

# Noah A. Smith
# 2/21/08
# Code for maximum likelihood estimation of a bigram HMM from 
# column-formatted training data.

# Usage:  train_hmm.py tags text > hmm-file

# The training data should consist of one line per sequence, with
# states or symbols separated by whitespace and no trailing whitespace.
# The initial and final states should not be mentioned; they are 
# implied.  
# The output format is the HMM file format as described in viterbi.pl.

import sys,re
from itertools import izip
from collections import defaultdict

TAG_FILE=sys.argv[1]
TOKEN_FILE=sys.argv[2]

vocab={}
OOV_WORD="OOV"
INIT_STATE="init"
FINAL_STATE="final"

emissions={}
bi_transitions={}
tri_transitions={}
transitionsTotal=defaultdict(int)
emissionsTotal=defaultdict(int)
length = 39832*1
with open(TAG_FILE) as tagFile, open(TOKEN_FILE) as tokenFile:       
        index = 1
	for tagString, tokenString in izip(tagFile, tokenFile):
                if index > length:
                        #print index
                        break
                index += 1
                #print length
		tags=re.split("\s+", tagString.rstrip())
		tokens=re.split("\s+", tokenString.rstrip())
		pairs=zip(tags, tokens)

		prevtag=INIT_STATE
		prevprevtag = INIT_STATE
		for (tag, token) in pairs:

			# this block is a little trick to help with out-of-vocabulary (OOV)
			# words.  the first time we see *any* word token, we pretend it
			# is an OOV.  this lets our model decide the rate at which new
			# words of each POS-type should be expected (e.g., high for nouns,
			# low for determiners).

			if token not in vocab:
                                #print token
				vocab[token]=1
				token=OOV_WORD

			if tag not in emissions:
				emissions[tag]=defaultdict(int)
			if (prevprevtag, prevtag, tag) not in tri_transitions:
				tri_transitions[(prevprevtag, prevtag, tag)]=0
                        if (prevtag, tag) not in bi_transitions:
                                bi_transitions[(prevtag, tag)] = 0

			# increment the emission/transition observation
			emissions[tag][token]+=1
			emissionsTotal[tag]+=1
			
			tri_transitions[(prevprevtag, prevtag, tag)]+=1
			bi_transitions[(prevtag, tag)] += 1
			transitionsTotal[prevtag] += 1

                        prevprevtag = prevtag
			prevtag=tag

		# don't forget the stop probability for each sentence
		if (prevprevtag, prevtag, FINAL_STATE) not in tri_transitions:
			tri_transitions[(prevprevtag, prevtag, FINAL_STATE)]=0
                if (prevtag, FINAL_STATE) not in bi_transitions:
                        bi_transitions[(prevtag, FINAL_STATE)] = 0
                        
		tri_transitions[(prevprevtag, prevtag, FINAL_STATE)]+=1
		bi_transitions[(prevtag, FINAL_STATE)]+= 1
		transitionsTotal[prevtag]+=1
			
for (prevprevtag,prevtag,tag) in tri_transitions:
	print "tri_trans %s %s %s %s" % (prevprevtag, prevtag, tag, float(tri_transitions[(prevprevtag, prevtag, tag)]) / bi_transitions[(prevtag,tag)])

for (prevtag,tag) in bi_transitions:
        print "bi_trans %s %s %s" % (prevtag, tag, float(bi_transitions[(prevtag, tag)]) / transitionsTotal[prevtag])
for tag in emissions:
	for token in emissions[tag]:
		print "emit %s %s %s " % (tag, token, float(emissions[tag][token]) / emissionsTotal[tag])



