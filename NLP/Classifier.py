import os 
import pickle
import random
import pandas as pd
import numpy as np
import pickle

class Classifier:
    
    def __init__(self):
        self.dir = os.path.dirname(os.path.realpath(__file__))

        
    def set_vectorizer(self, vectorizer):
        self.vectorizer = vectorizer
        vec_file = self.dir + '/models/vecs/' + vectorizer + '.pickle'
        if os.path.isfile(vec_file):
            with open(vec_file, 'rb') as f:
                vectorized_model = pickle.load(f)
                self.df = vectorized_model[0]
        
      
    def set_classifier(self, classifier):
        self.classifier = classifier

    def prepare_test_train_set(self, pct, random_seed=13, pct_evaluation=0.8):

        dataset = None
        if not hasattr(self, 'eval_df'):
            #First time, then, get the evaluation set:
            # Choose which indices will belong to each set
            num_articles = self.df.shape[0]
            idx = range(num_articles)
            self.df.index = idx
            #print(idx)
            num_train_test = int(num_articles * pct_evaluation)
            num_evaluation = num_articles - num_train_test
            train_test_idx = random.sample(idx, num_train_test)
            eval_idx = [x for x in idx if x not in train_test_idx]

            # Constructing the training and test sets
            self.traintest_df = self.df.iloc[train_test_idx]
            self.eval_df = self.df.iloc[eval_idx]


        if random_seed:
            random.seed(random_seed)
            
        # Choose which indices will belong to each set
        num_articles = self.traintest_df.shape[0]
        idx = range(num_articles)
        self.traintest_df.index = idx
        num_train = int(num_articles * pct)
        num_test = num_articles - num_train
        train_idx = random.sample(idx, num_train)
        test_idx = [x for x in idx if x not in train_idx]

        # Constructing the training and test sets
        self.train_df = self.traintest_df.iloc[train_idx]
        self.test_df = self.traintest_df.iloc[test_idx]

    def train_model(self):
        """ 
        Trains the classifier model
        """
        # Turn the training data frame into an appropriate
        # matrix / vector
        y = self.train_df['y']
        self.eqID = self.train_df['eqID']
        X = self.train_df.copy()
        del X['y']
        del X['eqID']
        del X['tweetID']

        print(X.shape)
        # exit()

        # Train the model
        self.classifier.fit(X,y)

    def predict_labels(self, dataset):
        """
        Predicts the labels of the test set
        """
        # Turn the test data frame into an appropriate
        # matrix / vector
        X = dataset.copy()
        del X['y']
        del X['eqID']
        del X['tweetID']

        # Predict the label of the test examples
        self.ypred = self.classifier.predict(X)
        
    def evaluate_results(self, dataset):
        # Check the predictions against observed values
        y = np.array(dataset['y'])
        y = y.astype(float)
        ypred = self.ypred
        # print(type(y))
        # print(type(ypred))
        # print(y)
        # print(ypred)
        mean_squared_error = ((y-ypred)**2).mean(axis=None)
        return mean_squared_error

        
    def bootstrap(self, iters=100, pct=0.8, pct_evaluation=0.8):

        results = []
        for i in range(iters):
            print("Iteration:["+str(i)+"]")
            self.prepare_test_train_set(pct=pct, pct_evaluation =pct_evaluation)
            self.train_model()
            self.predict_labels(self.train_df)
            stats = self.evaluate_results(self.train_df)
            self.predict_labels(self.eval_df)
            stats_eval = self.evaluate_results(self.eval_df)
            results.append(stats)
            print("results iter:" + str(i) + " : Test Error: " + str(stats) + " Evaluation error: " + str(stats_eval) )
        return results
        

    def evaluate_models(self, model_list):
        """
        
        Model is 
        {'name':'some_name',
        'vectorizer_pickle_filename':'tfidf', 
        'classifier':ActualClassifierObject} 
        """
        iters = 2
        pct = 0.75
        pct_evaluation = 0.8
        
        for model in model_list:
            print(('Now testing %s') % (model['name']))
            self.set_classifier(model['classifier'])
            self.set_vectorizer(model['vectorizer_pickle_filename'])
            self.name = model['name']
            results = self.bootstrap(iters=iters, pct=pct, pct_evaluation=pct_evaluation)
            model['results'] = results
        
            print("Results for model %s " %(model['name']))
            print(results)

        self.save_model()
            
    def save_model(self):
        # Either use the specified models name or pick a
        # numbered models name that has not been used yet
        model_dir = self.dir+'/models/classifier'
        print('Saving models ...')

        object_to_be_saved = self.classifier
        

        
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
            pickle.dump(self.classifier, f, protocol=2)
            print("Model saved " + filename)