### Train the weighted master vocab V_m using word2vec

import json, pprint, nltk, os, re
import numpy as np
from gensim.models import Word2Vec as w2v


## Read data from json files
json_file = "../Tweets/Tweets_earthquakes_conterminousUS_2008-2018_mag>=4_count=1147.json"
with open(json_file) as json_data:
	data = json.load(open(json_file))
	json_data.close()



## Preprocess the data into an array which can be processed by w2v
tokenSet = []
magLabels = []
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')  # Keep only alphanumeric characters as tokens
for idx_e in range(len(data)):
	for idx_n in range(len(data[idx_e]["tweets"])):
		text = data[idx_e]["tweets"][idx_n]["text"]
		text = re.sub(r"http\S+", "", text)       # remove urls
		text = text.lower()                       # convert to lowercase
		tokens = tokenizer.tokenize(text)         # tokenize
		tokenSet.append(tokens)
		magLabels.append(data[idx_e]["magnitude"])  # every tokenized tweet has a magnitude label



# Remove stopwords, numbers, singleton characters, and lemmatize
stopwords_nltk = nltk.corpus.stopwords.words('english')
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
tokenSet = [[lemmatizer.lemmatize(token) for token in doc if not (token in stopwords_nltk or token.isnumeric() or len(token) <= 1)] for doc in tokenSet] # remove stopwords

print('Preprocessing Completed. Total earthquakes: ', len(data), '. Total tweets: ', len(tokenSet))

print(tokenSet[0:10])




### Deploy w2v
model = w2v(tokenSet[0:20], min_count=1, size=10)
print('Vector for \'earthquake\': ', model['earthquake'])
