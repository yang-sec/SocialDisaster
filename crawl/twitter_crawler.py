import psycopg2
import json
import re
import got  # twitter library for historical data.
import time
import datetime


def connect_to_postgresql():
    try:
        conn = psycopg2.connect("dbname='earthq' user='educoder' host='localhost' password='educoder'")
        print("Connected")

        cur = conn.cursor()

        cur.execute("""SELECT * from test""")
        rows = cur.fetchall()

        print("showing data")

        for row in rows:
            print(row[0])


    except:
        print("Connection error")
    finally:
        cur.close()
        conn.close()


def create_table():
    try:
        conn = psycopg2.connect("dbname='earthq' user='educoder' host='localhost' password='educoder'")

        cur = conn.cursor()

        cur.execute("""select exists
             (  select 1
                from information_schema.tables
                where table_catalog = 'earthq'
                and table_name = 'posts'
             );
        """)
        rows = cur.fetchall()

        print rows
        for row in rows:
            if row[0] is False:
                # Table has not been created, hence, create it.
                print("Creating table, it did not exist before")
                cur.execute("""
                    create table posts (
                        location VARCHAR(255),
                        magnitude REAL, 
                        time     TIMESTAMP,
                        source   VARCHAR(20),
                        post     VARCHAR(5000)
                    );""")
                conn.commit()

            print(row[0])

    except:
        print("Connection error")

    finally:
        cur.close()
        conn.close()


def insert_into_db(place, magnitude, time, source, list_posts):
    if len(list_posts) > 0:
        try:
            conn = psycopg2.connect("dbname='earthq' user='educoder' host='localhost' password='educoder'")
            cur = conn.cursor()

            for post in list_posts:
                query = "insert into posts values (%s, %s, %s, %s , %s)"
                datet = datetime.datetime.fromtimestamp(time / 1000)
                data = (place, magnitude, datet, source, post)
                cur.execute(query, data)

            conn.commit()
        except psycopg2.Error as e:
            print("Connection error")
            print(e.pgerror)

        finally:
            cur.close()
            conn.close()


def read_earthquake_json(json_file):
    find_city_pattern = re.compile(r'.* of (.*)')

    # 1. First load from json
    data = json.load(open(json_file))
    features = data['features']
    for feature in features:
        properties = feature['properties']

        # 1.2 Just fetch from Twitter when the place matches expression ".* of .*"
        # Usually places have names like "200km of Oakton, Virginia" 
        matches = find_city_pattern.match(properties['place'])
        if matches:
            actual_city = matches.group(1)
            print("Place:" + actual_city + ', magnitude= ' + str(properties['mag']) + ", time=" + str(
                properties['time']))
            tweets = get_tweets(actual_city, properties['time'], max_tweets=1000)
            if len(tweets) > 0:
                print("\tTweets: > " + tweets[0])
                insert_into_db(actual_city, properties['mag'], properties['time'], 'Twitter', tweets)

    # Json: {features:[{properties:{mag:4.5,place:"2km WSW of Diablo, CA",time:"1519186937910"}}]}


def get_tweets(place, date_of_earthq_millisec, max_tweets=10):
    # seconds in two days:
    four_days_seconds = 345600
    date_of_earthq_secs = date_of_earthq_millisec / 1000
    lower_bound_date = time.strftime("%Y-%m-%d", time.gmtime(date_of_earthq_secs))
    upper_bound_date = time.strftime("%Y-%m-%d", time.gmtime(date_of_earthq_secs + four_days_seconds))

    tweetCriteria = got.manager.TweetCriteria().setNear("\"" + place + "\"").setWithin("15mi").setSince(
        lower_bound_date).setUntil(upper_bound_date).setMaxTweets(max_tweets)
    # tweetCriteria = got.manager.TweetCriteria().setQuerySearch('Earthquake').setSince("2017-09-18").setUntil("2017-09-30").setNear("\"Mexico City, Mexico\"").setWithin("40mi").setMaxTweets(1)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    return_tweets = []
    for tweet in tweets:
        return_tweets.append(tweet.text)

    return return_tweets


# connect_to_postgresql()
create_table()

earthquake_data_json_path = "app/static/js/data/usgsEarthquacks_7days.json"
read_earthquake_json(earthquake_data_json_path)
