from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfVectorizerB:
    
    def __init__(self, stop_words = 'english', min_df = 5, max_df= 0.5):
        
        self.vectorizer = TfidfVectorizer(stop_words = stop_words, min_df = min_df, max_df = max_df)
        
    def fit(self, sentences):
        
        new_sentences = [' '.join(x) for x in sentences]
        
        self.vectorizer.fit(new_sentences)
        
    def transform(self, sentences):
        new_sentences = [' '.join(x) for x in sentences]
        return self.vectorizer.transform(new_sentences)