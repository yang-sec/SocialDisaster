# Damage Assessment with Remote Sensing and Social Media (codename: SocialDisaster)
This project provides an interesting method for earthquake damage assessment.

## Data
1. Get a list of earthquakes from an official data outlet, such as USGS or an official Twitter account. Each earthquake item should have the following format: e=[latitude,longtitude,time,magnitude]. Group them by magnitude.

## MasterVocab

## Database

## GUI

## Crawlers

### Earthquake crawler

Based off USGS data. To start it up, go to 

```
cd crawl
python earthquake_crawler.py
```

There will be a file created in the crawl folder with the earthquake data of the last 7 days (configurable in the python script). 

