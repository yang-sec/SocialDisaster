import os
import json
import pickle
from sklearn.ensemble import RandomForestRegressor
from TfidfVectorizerB import TfidfVectorizerB
import pandas as pd
import numpy as np

# Before running this,
#   python crawl/twitter_crawler.py
#   python NLP/vectorizer_test.py
#   python NLP/classifier_test.
#   python NLP/evaluate_earthquake_tweets.py


dir = os.path.dirname(os.path.realpath(__file__))


raw_crawl_file = "Tweets_earthquakes_world_2018_mag>=5_count=337.json"
earthquake_tweets_vectorization_file = dir + "/../NLP/models/vecs/" + "tfidf_2018.pickle"
earthquake_tweets_classifier_file = dir + "/../NLP/models/classifier/" + "randomforest_tfidf_2018.pickle"
'''
raw_crawl_file = "Tweets_earthquakes_conterminousUS_2008-2018_mag>=4_count=1147.json"
earthquake_tweets_vectorization_file = dir + "/../NLP/models/vecs/" + "tfidf_2008-2018.pickle"
earthquake_tweets_classifier_file = dir + "/../NLP/models/classifier/" + "randomforest_tfidf_2008-2018.pickle"
'''

earthquake_tweets_output_file = dir + "/../app/static/js/data/Evaluated_" + raw_crawl_file

# 1 reads earthquake tweets
earthquake_tweets_file = dir + "/../Tweets/" + raw_crawl_file
earthquake_tweets_crawl_file = open(earthquake_tweets_file)
earthquakes_tweets_raw = json.load(earthquake_tweets_crawl_file)
earthquake_tweets_crawl_file.close()
print("Earthquake tweets crawled file loaded " + earthquake_tweets_file)

# 2 reads earthquake tweets vectorization
earthquake_tweets_dataframe = open(earthquake_tweets_vectorization_file, 'rb')
vectorized_model = pickle.load(earthquake_tweets_dataframe)
earthquake_tweets_dataframe = vectorized_model[0]
earthquake_tweets_vocabulary = vectorized_model[1]
earthquake_tweets_vocabulary_inv = {v: k for k, v, in earthquake_tweets_vocabulary.items()}
print("Earthquake tweets vectorizations loaded " + earthquake_tweets_vectorization_file)

# 3 reads classifier
classifier_file = open(earthquake_tweets_classifier_file, 'rb')
classifier = pickle.load(classifier_file)
print("Earthquake tweets classifier loaded " + earthquake_tweets_classifier_file)

# 4 for each earthquake, for each tweet, get vector, evaluate, append to json file.
print("evaluating " + str(len(earthquakes_tweets_raw)) + " earthquakes.")
a = 0
for earthquake_tweets in earthquakes_tweets_raw:
    a = a + 1
    print("evaluating ("+ str(a) + ")th earthquake, with " + str(len(earthquake_tweets['tweets'])) + " tweets.")
    predicted_tweet_scores = []
    # below we filter down the vectors to only the earthquake related tweets vectors
    filtered_dataframe = earthquake_tweets_dataframe.loc[earthquake_tweets_dataframe['eqID'] == earthquake_tweets['id']]
    b = 0

    condense_vocab = None

    for tweet in earthquake_tweets['tweets']:
        b = b + 1
        # print(b)
        # below we fetch the tweet vector
        tweet_vector = filtered_dataframe.loc[filtered_dataframe['tweetID'] == tweet['id']]



        del tweet_vector['y']
        del tweet_vector['eqID']
        del tweet_vector['tweetID']
        # print(tweet_vector)
        predicted_tweet_score = classifier.predict(tweet_vector)
        #print(predicted_tweet_score)
        tweet['predicted_magnitude'] = float(predicted_tweet_score[0])
        predicted_tweet_scores.append(predicted_tweet_score[0])

        tweet_vector_np = tweet_vector.as_matrix()
        tweet_vector_np = tweet_vector_np.reshape((-1,))
        tweet_vector_np = tweet_vector_np.astype(np.float)
        if condense_vocab is None:
            condense_vocab = tweet_vector_np
        else:
            condense_vocab = condense_vocab + tweet_vector_np
        # print(tweet_vector_np)

        # exit()

    earthquake_tweets['predicted_magnitude_average'] = np.mean(np.array(predicted_tweet_scores))
    #print(predicted_tweet_scores)
    #print(np.array(predicted_tweet_scores))
    earthquake_tweets['predicted_magnitude_max'] = float(np.amax(np.array(predicted_tweet_scores)))
    earthquake_tweets['predicted_magnitude_min'] = float(np.amin(np.array(predicted_tweet_scores)))
    earthquake_tweets['predicted_magnitude_stddev'] = float(np.std(np.array(predicted_tweet_scores)))

    condense_vocab_list = []
    condense_vocab = condense_vocab * 100 / np.max(condense_vocab)
    for i in range(0,len(condense_vocab)):
        condense_vocab_list.append((condense_vocab[i]  * -1, earthquake_tweets_vocabulary_inv[i]))
    condense_vocab_list.sort()
    master_vocab_sorted = [[element[1], element[0] * -1] for element in condense_vocab_list if element[0] *-1 > 0.0]
    #condense_vocab = np.sort(condense_vocab*(-1)) * (-1)
    # print(master_vocab_sorted)
    # exit()
    earthquake_tweets['master_vocab'] = master_vocab_sorted


# dumping vocabulary
# earthquakes_tweets_raw['vocabulary'] = earthquake_tweets_vocabulary


# 5 save final json file for web app / DB consumption
with open(earthquake_tweets_output_file, 'w') as out:
    json.dump(earthquakes_tweets_raw, out)