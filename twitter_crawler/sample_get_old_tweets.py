import got
# https://github.com/Jefferson-Henrique/GetOldTweets-python
# pip install pyquery
# pip install lxml

#tweetCriteria = got.manager.TweetCriteria().setNear("\"San Francisco, California\"").setWithin("15mi").setSince("2016-03-01").setUntil("2016-03-22").setMaxTweets(20)
tweetCriteria = got.manager.TweetCriteria().setQuerySearch('Earthquake').setSince("2017-09-18").setUntil("2017-09-30").setNear("\"Mexico City, Mexico\"").setWithin("40mi").setMaxTweets(20)
tweets = got.manager.TweetManager.getTweets(tweetCriteria)
for tweet in tweets:
    print(tweet.text)

