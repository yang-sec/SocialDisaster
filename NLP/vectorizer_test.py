from Vectorizer import Vectorizer


vect = Vectorizer('tfidf','tfidf')
vect.vectorize("Tweets/Tweets_earthquakes_conterminousUS_2008-2018_mag>=4_count=1147.json")
vect.save_model()
print("Finished vectorizing")