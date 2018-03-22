# Damage Assessment with Remote Sensing and Social Media (codename: SocialDisaster)
This project provides an interesting method for earthquake damage assessment.

## Process USGS JSON file

```
python3 processRawJSON.py
```
It will parse the ras JSON file and generate a numpy array for data analysis and NLP tasks.


## Earthquake crawler

Based off USGS data. To start it up, go to 
```
cd crawl
python earthquake_crawler.py
```
There will be a file created in the crawl folder with the earthquake data of the last 7 days (configurable in the python script). 

