import math, collections

class BackoffModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.total = 0
    self.unitotal = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    # Tip: To get words from the corpus, try
    #    for sentence in corpus.corpus:
    #       for datum in sentence.data:  
    #         word = datum.word
    for sentence in corpus.corpus:
      for i in range(len(sentence.data)):  
        token = sentence.data[i].word
        #print token
        self.unigramCounts[token] = self.unigramCounts[token] + 1
        self.total += 1
        self.unitotal += 1
        if token != '</s>':
          nextToken = sentence.data[i+1].word
          self.bigramCounts[(token,nextToken)] = self.bigramCounts[(token,nextToken)] + 1
          #print (token,nextToken)
    #print self.unigramCounts['the']
    #print len(self.bigramCounts)
    #print len(self.unigramCounts)
    #print self.total
    for key, value in self.unigramCounts.iteritems():
      self.unigramCounts[key] = self.unigramCounts[key] + 1
    self.total += len(self.unigramCounts)
    #self.total += len(self.unigramCounts)
    #print self.total

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score1 = 0.0
    score2 = 0.0
    for i in range(len(sentence)):
      if sentence[i] != '</s>':
        countbi = self.bigramCounts[(sentence[i], sentence[i+1])]
        #print countbi
        if countbi > 0:
          #print (sentence[i], sentence[i+1])
          #print countbi
          countuni = self.unigramCounts[sentence[i]]
          #print countuni
          
          score1 += math.log(countbi)
          score1 -= math.log(countuni)
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
      
    return 0.025*score1 + 0.1*score2
