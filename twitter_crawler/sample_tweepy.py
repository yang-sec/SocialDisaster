import tweepy # install with pip3 install tweepy
from geopy.geocoders import Nominatim # install with pip3 install geopy
import sample_tweepy_config as cfg

auth = tweepy.OAuthHandler(cfg.educoder01['consumer_key'], cfg.educoder01['consumer_secret'])
auth.set_access_token(cfg.educoder01['access_token'], cfg.educoder01['access_token_secret'])

api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# print(public_tweets)
# for tweet in public_tweets:
#     print(tweet.text)


# Build location filter:
# From API notes here: http://docs.tweepy.org/en/v3.5.0/api.html#API.search
#   The location is preferentially taking from the Geotagging API, but will fall back to their Twitter profile.

# Search tweets in New Your from beginning of the year until Feb 10th:
print("Search tweets in New Your from beginning of the year until Feb 10th:")
strlocation = "New York,NY"
geolocator = Nominatim()
geolocation = geolocator.geocode(strlocation)
print((geolocation.latitude, geolocation.longitude))
radius = "100mi" # if km, then use 40km
geocode = "" + str(geolocation.latitude) + "," + str(geolocation.longitude) + "," + radius
results = api.search(q="Machine Learning", lang="en", rpp=1, geocode=geocode, since="2018-03-11", until="2018-03-20")
for tweet in results:
    #if tweet.geo != None: # HEre is how we filter by the tweets that actually have geotagging.
    print(tweet.text)


# Now we search an old date:
print("Now we search an old date:")
#strlocation = "Falls Church,VA"
#strlocation = "Mexico City,Mexico"
results = api.search(q="Machine Learning", lang="en", rpp=1, geocode=geocode, since="2017-01-01", until="2017-02-10")
for tweet in results:
    #if tweet.geo != None: # HEre is how we filter by the tweets that actually have geotagging.
    print(tweet.text)




