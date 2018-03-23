import json
import re
import time
from bs4 import BeautifulSoup
import requests
#pip install beautifulsoup4 --user
#pip install requests --user

class news_crawler:
    
    def __init__(self, file_name):
        self.folder = "./UsgsData/"
        self.file = file_name
    
    def crawl_news(self):
        find_city_pattern = re.compile(r'.* of (.*)')
        with open(self.folder + self.file, 'r') as f:
            data = json.load(f)
            

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
                    if properties['mag'] > 5.0:
                        news = self.get_items(actual_city, properties['time'], max_items=1000)
                        #tweets = get_tweets(actual_city, properties['time'], max_tweets=1000)
                        #if len(tweets) > 0:
                        #    print("\tTweets: > " + tweets[0])
                    
    def get_items(self,actual_city, timestamp, max_items):
        # seconds in two days:
        four_days_seconds = 345600
        date_of_earthq_secs = timestamp / 1000
        lower_bound_date = time.strftime("%d %b %Y", time.gmtime(date_of_earthq_secs))
        upper_bound_date = time.strftime("%Y-%m-%d", time.gmtime(date_of_earthq_secs + four_days_seconds))
        
        #url = "https://news.google.com/news/search/section/q/earthquake%20" + actual_city + "%20" + lower_bound_date
        url = "https://news.google.com/news/search/section/q/earthquake%20" + lower_bound_date
        print url 
        html = requests.get(url, headers={'user-agent': 'Mozilla/5.0'}).text
        soup = BeautifulSoup(html, 'html.parser')
        
        links = soup.find_all('a')
        
        urls = []
        
        for link in links:
            if 'google' not in link['href']:
                if ' ' in link.get_text():
                    urls.append(link['href'])

        print urls


crawler = news_crawler("earthquakes_conterminousUS_2008-2018_mag>=4_count=1147.json")
crawler.crawl_news()

