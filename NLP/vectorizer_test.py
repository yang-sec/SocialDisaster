from Vectorizer import Vectorizer


# vect = Vectorizer('tfidf_world_2018','tfidf')
# vect.vectorize("Tweets/Tweets_earthquakes_world_2018_mag>=5_count=337.json")


# vect = Vectorizer('tfidf_US_2008-2018','tfidf')
# vect.vectorize("Tweets/Tweets_earthquakes_conterminousUS_2008-2018_mag>=4_count=1147.json")

vect = Vectorizer('tfidf_world_2008-2018','tfidf')
vect.vectorize("Tweets/Tweets_earthquakes_merged_2008-2018_count=20470.json")

vect.save_model()
print("Finished vectorizing")


