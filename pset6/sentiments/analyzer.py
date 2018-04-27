import nltk

class Analyzer():
    """Implements sentiment analysis."""
    
    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        
        self.positives = set()        

        with open(positives, "r") as file:
            for line in file:
                if line.startswith(";"):
                    continue
                else:
                    self.positives.add(line.strip())
                    
        self.negatives = set()        

        with open(negatives, "r") as file:
            for line in file:
                if line.startswith(";"):
                    continue
                else:
                    self.negatives.add(line.strip())
        
    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""

        # instantiate tokenizer
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        
        total = 0

        # iterate over tokens
        for word in tokens:
            if word.lower() in self.positives:
                total += 1
            elif word.lower() in self.negatives:
                total -= 1
            else:
                continue

        return total