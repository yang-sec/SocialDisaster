
import json
import re
import time
import datetime
import got
from merge_earthquakes import merge_earthquake



def read_earthquake_json(json_file, output_file):
    find_city_pattern = re.compile(r'.* of (.*)')

    # 1. First load from json
    earthquake_merger = merge_earthquake(time_threshold_seconds=86400, distance_threshold_km=20)
    data = earthquake_merger.merge_file(json_file)
    #data = json.load(open(json_file))
    features = data['features']
    earthquake_list = []
    iteration = 0
    for feature in features:
        properties = feature['properties']

        # 1.2 Just fetch from Twitter when the place matches expression ".* of .*"
        # Usually places have names like "200km of Oakton, Virginia" 
        matches = find_city_pattern.match(properties['place'])
        if matches:
            actual_city = matches.group(1)
            print("Place:" + actual_city + ', magnitude= ' + str(properties['mag']) + ", time=" + str(
                properties['time']))
            tweets = get_tweets(actual_city, properties['time'], max_tweets=100)
            #if len(tweets) > 0:
                #print("\tTweets: > ", tweets[0].id, tweets[0].username, tweets[0].permalink, tweets[0].date, tweets[0].text,
                #  tweets[0].retweets, tweets[0].favorites, tweets[0].mentions, tweets[0].hashtags, tweets[0].geo)

            earthquake = {}
            earthquake['id'] = feature['id']
            earthquake['actual_city'] = actual_city
            earthquake['occurence_timestamp'] = properties['time']
            earthquake['occurence_date'] = time.strftime("%d %b %Y", time.gmtime(properties['time']/1000))
            earthquake['coordinates'] = feature['geometry']['coordinates']
            earthquake['magnitude'] = properties['mag']
            tweets_list = []
            earthquake['tweets'] = tweets_list
            
            for tweet in tweets:
                tweet_dic = {}
                tweet_dic['id'] = tweet.id
                tweet_dic['username'] = tweet.username
                tweet_dic['permalink'] = tweet.permalink
                tweet_dic['date'] = str(tweet.date)
                tweet_dic['favorites'] = tweet.favorites
                tweet_dic['text'] = tweet.text
                tweet_dic['retweets'] = tweet.retweets
                tweet_dic['mentions'] = tweet.mentions
                tweet_dic['hashtags'] = tweet.hashtags
                tweet_dic['geo'] = tweet.geo
                
                print("\tTweets: > ", tweet.id, tweet.username,tweet.permalink, tweet.date, tweet.text, tweet.retweets,tweet.favorites, tweet.mentions, tweet.hashtags, tweet.geo)
                tweets_list.append(tweet_dic)
                #insert_into_db(actual_city, properties['mag'], properties['time'], 'Twitter', tweets)
            
            
            if len(tweets) > 0:
                earthquake['tweets'] = tweets_list
                earthquake_list.append(earthquake)
                with open(output_file, 'w') as out:
                    json.dump(earthquake_list, out)
            
            iteration = iteration + 1
                    
    if len(earthquake_list) > 0:
        with open(output_file, 'w') as out:
            json.dump(earthquake_list, out)
    # Json: {features:[{properties:{mag:4.5,place:"2km WSW of Diablo, CA",time:"1519186937910"}}]}


def get_tweets(place, date_of_earthq_millisec, max_tweets=10):
    # seconds in two days:
    four_days_seconds = 345600
    date_of_earthq_secs = date_of_earthq_millisec / 1000
    lower_bound_date = time.strftime("%Y-%m-%d", time.gmtime(date_of_earthq_secs))
    upper_bound_date = time.strftime("%Y-%m-%d", time.gmtime(date_of_earthq_secs + four_days_seconds))

    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('earthquake').setNear("\"" + place + "\"").setWithin("15mi").setSince(
        lower_bound_date).setUntil(upper_bound_date).setMaxTweets(max_tweets)
    # tweetCriteria = got.manager.TweetCriteria().setQuerySearch('Earthquake').setSince("2017-09-18").setUntil("2017-09-30").setNear("\"Mexico City, Mexico\"").setWithin("40mi").setMaxTweets(1)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    return_tweets = []
    for tweet in tweets:
        return_tweets.append(tweet)

    return return_tweets


# connect_to_postgresql()
# create_table()

#file_name = "earthquakes_conterminousUS_2008-2018_mag>=4_count=1147.json"
file_name = "earthquakes_world_2018_mag>=5_count=337.json"

file_without_ext = file_name.split(".")

output_file = "../Tweets/Tweets_" + file_without_ext[0] + ".json"
#earthquake_data_json_path = "../UsgsData/earthquakes_conterminousUS_2008-2018_mag>=4_count=1147.json"
earthquake_data_json_path = "../UsgsData/" +file_name
read_earthquake_json(earthquake_data_json_path, output_file)
