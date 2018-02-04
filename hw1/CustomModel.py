import math, collections
class CustomModel:

  def __init__(self, corpus):
    """Initial custom language model and structures needed by this mode"""
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.trigramCounts = collections.defaultdict(lambda: 0)
    self.quagramCounts = collections.defaultdict(lambda: 0)
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model.
    """  
    # TODO your code here
    for sentence in corpus.corpus:
      for i in range(len(sentence.data)):  
        token = sentence.data[i].word
        #print token
        self.unigramCounts[token] = self.unigramCounts[token] + 1
        self.total += 1
        if token != '</s>':
          nextToken = sentence.data[i+1].word
          self.bigramCounts[(token,nextToken)] = self.bigramCounts[(token,nextToken)] + 1
          self.totalbi += 1
          if sentence.data[i+1].word != '</s>':
            nextnext = sentence.data[i+2].word
            self.trigramCounts[(token,nextToken,nextnext)] = self.trigramCounts[(token,nextToken,nextnext)] + 1
            if sentence.data[i+2].word != '</s>':
              nextnextnext = sentence.data[i+3].word
              self.quagramCounts[(token,nextToken,nextnext,nextnextnext)] = self.quagramCounts[(token,nextToken,nextnext,nextnextnext)] + 1
          #print (token,nextToken)
    #print self.unigramCounts['the']
    #print len(self.bigramCounts)
    #print len(self.unigramCounts)
    #print len(self.trigramCounts)
    #print self.total
    for key, value in self.unigramCounts.iteritems():
      self.unigramCounts[key] = self.unigramCounts[key] + 1
    self.total += len(self.unigramCounts)
    #print self.total

  def score(self, sentence):
    """ With list of strings, return the log-probability of the sentence with language model. Use
        information generated from train.
    """
    # TODO your code here
    score1 = 0.0
    score2 = 0.0
    score3 = 0.0
    score4 = 0.0
    for i in range(len(sentence)):
      if sentence[i] != '</s>':
        if sentence[i+2] != '</s>':
          countqua = self.quagramCounts[(sentence[i], sentence[i+1],sentence[i+2],sentence[i+3])]
          if countqua > 0:
            counttri = self.trigramCounts[(sentence[i], sentence[i+1],sentence[i+2])]
            score4 += math.log(countqua)
            score4 -= math.log(counttri)
          else:
            if sentence[i+1] != '</s>':
              counttri = self.trigramCounts[(sentence[i], sentence[i+1],sentence[i+2])]
              if counttri > 0:
                countbi = self.bigramCounts[(sentence[i], sentence[i+1])]
                score3 += math.log(counttri)
                score3 -= math.log(countbi)
              else:
                countbi = self.bigramCounts[(sentence[i], sentence[i+1])]
                #print countbi
                if countbi > 0:
                  #print (sentence[i], sentence[i+1])
                  #print countbi
                  countuni = self.unigramCounts[sentence[i]]
                  #print countuni
                  
                  score1 += math.log(countbi)
                  score1 -= math.log(countuni + len(self.unigramCounts))
                else:#use smoothed unigram
                  #print count
                  countuni = self.unigramCounts[sentence[i]]
                  #print count
                  if countuni > 0:
                    score2 += math.log(countuni)
                    score2 -= math.log(self.total)
                  else:
                    score2 += math.log(1)
                    score2 -= math.log(self.total)
    #print score1
    #print score2
    #print score3
    return 0.001*score1 + 0.1*score2 + 0.01*score3
