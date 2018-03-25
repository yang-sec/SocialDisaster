from Classifier import Classifier
from sklearn.ensemble import RandomForestRegressor

cls = RandomForestRegressor()

classifier = Classifier()
models=[
    {
        'name':"tfidf-randomforest",
        'vectorizer_pickle_filename': "tfidf",
        'classifier': cls
    }
]
classifier.evaluate_models(models)
