import math, collections

class SmoothUnigramModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.total = 0
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
    self.unigramCounts['UNK'] = 0
    for sentence in corpus.corpus:
      for datum in sentence.data:  
        token = datum.word
        #print token
        self.unigramCounts[token] = self.unigramCounts[token] + 1
        self.total += 1
    #print self.unigramCounts['the']
    for key, value in self.unigramCounts.iteritems():
      self.unigramCounts[key] = self.unigramCounts[key] + 1
      self.total += 1
    #print self.unigramCounts['the']
    

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0 
    for token in sentence:
      count = self.unigramCounts[token]
      if count > 0:
        score += math.log(count)
        score -= math.log(self.total)
      else:
        count = self.unigramCounts['UNK']
        #print count
        score += math.log(count)
        score -= math.log(self.total)
        #self.unigramCounts['UNK'] = self.unigramCounts['UNK'] + 1
        #self.total += 1
    return score
