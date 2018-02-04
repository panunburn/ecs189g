import math, collections

class SmoothBigramModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
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

    for sentence in corpus.corpus:
      for i in range(len(sentence.data)):  
        token = sentence.data[i].word
        #print token
        self.unigramCounts[token] = self.unigramCounts[token] + 1
        self.total += 1
        if token != '</s>':
          nextToken = sentence.data[i+1].word
          self.bigramCounts[(token,nextToken)] = self.bigramCounts[(token,nextToken)] + 1
    #print self.unigramCounts['the']
    for key, value in self.bigramCounts.iteritems():
      self.bigramCounts[key] = self.unigramCounts[key] + 1
      self.unigramCounts[key[0]] = self.unigramCounts[key[0]] + 1
      self.unigramCounts[key[1]] = self.unigramCounts[key[1]] + 1
      self.total += 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0
    for i in range(len(sentence)):
      if sentence[i] != '</s>':
        count = self.bigramCounts[(sentence[i], sentence[i+1])]
        countuni = self.unigramCounts[sentence[i]]
        if count > 0:
          score += math.log(count)
          score -= math.log(countuni)
        else:
          #print count
          score += math.log(1)
          score -= math.log(self.total)
          #self.unigramCounts['UNK'] = self.unigramCounts['UNK'] + 1
          #self.total += 1
        
    return score
