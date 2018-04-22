import json

json_file = "../Tweets/Tweets_earthquakes_world_2018_mag>=5_count=337.json"

f = open(json_file)
data = json.load(f)
#print(data)

for earthq in data:
    for tweet in earthq['tweets']:
        if len(tweet['geo']) >= 0:
            print(tweet['geo'])
    
