# Damage Assessment with Remote Sensing and Social Media (codename: SocialDisaster)
This project provides an interesting method for earthquake damage assessment.

## Process USGS JSON file

```
python3 processRawJSON.py
```
It will parse the raw JSON file and generate a numpy array for data analysis and NLP tasks.


## Earthquake crawler

Based off USGS data. To start it up, go to 
```
cd crawl
python earthquake_crawler.py
```
There will be a file created in the crawl folder with the earthquake data of the last 7 days (configurable in the python script). 


## Use of vectorizer and classifier

Run the vectorizer example with "python NLP/vectorizer_test.py"

Then this will save the vectors in the folder NLP/models/vecs.

After that we can run the classifiers with code similar to "python NLP/classifier_test.py" which will read from the vectorizer files in "NLP/models/vecs".

Sequence thens hould be to run vectorizers first and then classifiers

