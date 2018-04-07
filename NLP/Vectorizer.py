from TfidfVectorizerB import TfidfVectorizerB
import  nltk, os, re
import json
import pandas as pd
import numpy as np
import pickle

class Vectorizer:
    
    def __init__(self, name, vectorizer_type):
        
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.name = name 
        
        tfidf = TfidfVectorizerB(stop_words="english", min_df=0.05, max_df=0.95)
        # w2v = W2V
        self.vectorizers = {
            'tfidf': tfidf
        }
        
        self.vectorizer = self.vectorizers[vectorizer_type]
        
    def vectorize(self, input_file):
        input_file_f = open(input_file)
        data = json.load(input_file_f)
        input_file_f.close()
        ## Preprocess the data into an array which can be processed by w2v
        tokenSet = []
        magLabels = []
        eqIDs = []
        tweetIDs = []
        tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')  # Keep only alphanumeric characters as tokens
        for idx_e in range(len(data)):
            for idx_n in range(len(data[idx_e]["tweets"])):
                text = data[idx_e]["tweets"][idx_n]["text"]
                text = re.sub(r"http\S+", "", text)  # remove urls
                text = text.lower()  # convert to lowercase
                tokens = tokenizer.tokenize(text)  # tokenize
                tokenSet.append(tokens)
                magLabels.append(data[idx_e]["magnitude"])  # every tokenized tweet has a magnitude label
                eqIDs.append(data[idx_e]['id'])
                tweetIDs.append(data[idx_e]['tweets'][idx_n]['id'])

        # Remove stopwords, numbers, singleton characters, and lemmatize
        stopwords_nltk = nltk.corpus.stopwords.words('english')
        lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
        tokenSet = [[lemmatizer.lemmatize(token) for token in doc if
                     not (token in stopwords_nltk or token.isnumeric() or len(token) <= 1)] for doc in
                    tokenSet]  # remove stopwords

        print('Preprocessing Completed. Total earthquakes: ', len(data), '. Total tweets: ', len(tokenSet))
        
        nSamples = len(tokenSet)
        #subsample = 20
        
        #Here we fit the vectorizer
        self.vectorizer.fit(tokenSet[0:nSamples])
        
        #Now we focus on adding the label:
        sentences = self.vectorizer.transform(tokenSet[0:nSamples])
        
        sentences_array = sentences.toarray()
        labels_array = np.array(magLabels[0:nSamples])
        labels_array = np.expand_dims(labels_array,axis=1)
        eqID_array = np.array(eqIDs[0:nSamples])
        eqID_array = np.expand_dims(eqID_array,axis=1)
        tweetIDs_array = np.array(tweetIDs[0:nSamples])
        tweetIDs_array = np.expand_dims(tweetIDs_array, axis=1)
        
        # print("labels_array dims")
        # print(labels_array.shape)
        # print("sentence_array dims")
        # print(sentences_array.shape)
        sentences_array = np.append(sentences_array,labels_array,axis=1)
        sentences_array = np.append(sentences_array,eqID_array,axis=1)
        sentences_array = np.append(sentences_array, tweetIDs_array, axis=1)

        
        
        # print(sentences_array[0:2])
        # print("finished vectorizing")
        
        df = pd.DataFrame(sentences_array)
        num_cols = df.shape[1]
        df = df.rename(columns={ df.columns[num_cols-3]: 'y' , df.columns[num_cols-2]: 'eqID' , df.columns[num_cols-1]: 'tweetID'})
        #df = df.rename(columns={df.columns[num_cols-2]: 'y'})
        #df = df.rename(columns={ df.columns[num_cols-1]: 'eqID' })
        self.model_df = df
        #print(df)
        
        
    def save_model(self):
        # Either use the specified models name or pick a
        # numbered models name that has not been used yet
        model_dir = self.dir+'/models/vecs'
        print('Saving models ...')

        object_to_be_saved = self.model_df
        rows_count = len(self.model_df.index)
        

        
        if self.name:
            filename = model_dir + '/' + self.name + '.pickle'
        else:
            files = os.listdir(model_dir)
            already_used = True
            i = 0
            while already_used:
                filename = 'model_'+ str(i) + '.pickle'
                if filename in files:
                    i += 1
                else:
                    already_used = False
            filename = model_dir + '/' + filename
        with open(filename, 'wb') as f:
            pickle.dump(self.model_df, f, protocol=2)
            print("Model saved " + filename)