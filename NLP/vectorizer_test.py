from Vectorizer import Vectorizer


vect = Vectorizer('tfidf_2018','tfidf')
vect.vectorize("Tweets/Tweets_earthquakes_world_2018_mag>=5_count=337.json")


'''
vect = Vectorizer('tfidf_2008-2018','tfidf')
vect.vectorize("Tweets/Tweets_earthquakes_conterminousUS_2008-2018_mag>=4_count=1147.json")
'''

vect.save_model()
print("Finished vectorizing")


