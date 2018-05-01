from Classifier import Classifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor

cls = RandomForestRegressor()
cls_SVR = SVR()
cls_MLPR = MLPRegressor(hidden_layer_sizes=(500, 250, 20))
classifier = Classifier()
models=[
    {
    	
        # 'name':"randomforest_tfidf_world_2018",
        # 'vectorizer_pickle_filename': "tfidf_world_2018",

        'name':"randomforest_tfidf_US_2008-2018",
        'vectorizer_pickle_filename': "tfidf_US_2008-2018",

        # 'name':"randomforest_tfidf_world_2008-2018",
        # 'vectorizer_pickle_filename': "tfidf_world_2008-2018",
        
        'classifier': cls_MLPR
    },
    {

        # 'name':"randomforest_tfidf_world_2018",
        # 'vectorizer_pickle_filename': "tfidf_world_2018",

        'name': "randomforest_tfidf_US_2008-2018",
        'vectorizer_pickle_filename': "tfidf_US_2008-2018",

        # 'name':"randomforest_tfidf_world_2008-2018",
        # 'vectorizer_pickle_filename': "tfidf_world_2008-2018",

        'classifier': cls_SVR
    },
    {

        # 'name':"randomforest_tfidf_world_2018",
        # 'vectorizer_pickle_filename': "tfidf_world_2018",

        'name': "randomforest_tfidf_US_2008-2018",
        'vectorizer_pickle_filename': "tfidf_US_2008-2018",

        # 'name':"randomforest_tfidf_world_2008-2018",
        # 'vectorizer_pickle_filename': "tfidf_world_2008-2018",

        'classifier': cls
    }
]
classifier.evaluate_models(models)
