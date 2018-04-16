from Classifier import Classifier
from sklearn.ensemble import RandomForestRegressor

cls = RandomForestRegressor()

classifier = Classifier()
models=[
    {
    	
        'name':"randomforest_tfidf_2018",
        'vectorizer_pickle_filename': "tfidf_2018",

        #'name':"randomforest_tfidf_2008-2018",
        #'vectorizer_pickle_filename': "tfidf_2008-2018",
        
        'classifier': cls
    }
]
classifier.evaluate_models(models)
