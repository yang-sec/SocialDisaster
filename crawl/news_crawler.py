import json
import re
import time
from bs4 import BeautifulSoup
import requests
from newspaper import Article 
from parse_places import abbrevation_to_long
from merge_earthquakes import merge_earthquake
#pip install git+https://github.com/codelucas/newspaper@python-2-head --user
#pip install beautifulsoup4 --user
#pip install requests --user

class news_crawler:
    
    def __init__(self, file_name, output_file_name):
        
        self.file = file_name
        self.output_file = output_file_name
        self.abbreviation_to_long = abbrevation_to_long()
        self.earthquake_merger = merge_earthquake(time_threshold_seconds=86400, distance_threshold_km=20)
    
    def crawl_news(self):
        find_city_pattern = re.compile(r'.* of (.*)')
       
        data = self.earthquake_merger.merge_file(self.file)
            
        earthquakes = []
        
        features = data['features']
        iteration = 0
        for feature in features:
            properties = feature['properties']
        
            # 1.2 Just fetch from Twitter when the place matches expression ".* of .*"
            # Usually places have names like "200km of Oakton, Virginia" 
            matches = find_city_pattern.match(properties['place'])
            if matches:
                actual_city = matches.group(1)
                query_city = actual_city.split(", ")
                if len(query_city) == 1:
                    query_city = query_city[0]
                elif len(query_city) > 1:
                    query_city = query_city[-1]
                query_city = self.abbreviation_to_long.get_long_name(query_city)
                print("Place:" + actual_city + ', magnitude= ' + str(properties['mag']) + ", time=" + str(
                    properties['time']))
                if properties['mag'] > 5.0:
                    earthquake_news = self.get_items(query_city, actual_city, properties['time'], properties['mag'], max_items=1000)
                    
                    if len(earthquake_news['news']) > 0:
                        iteration = iteration + 1
                        earthquakes.append(earthquake_news)
                        print iteration
                        #break
                        with open(self.output_file, 'w') as out:
                            json.dump(earthquakes, out)
                
    def get_items(self,query_city, actual_city , timestamp, magnitude, max_items):
        # seconds in two days:
        four_days_seconds = 345600
        date_of_earthq_secs = timestamp / 1000
        day_month_year = time.strftime("%d %b %Y", time.gmtime(date_of_earthq_secs))
        month_day_year = time.strftime("%b %d %Y", time.gmtime(date_of_earthq_secs))
        month_year = time.strftime("%b %Y", time.gmtime(date_of_earthq_secs))
        
        
        #url = "https://news.google.com/news/search/section/q/earthquake " + query_city + " " + day_month_year
        #url = "https://news.google.com/news/search/section/q/earthquake%20" + lower_bound_date
        url = "https://www.google.com/search?q=earthquake "+actual_city + " " + month_day_year+"&source=lnms&tbm=nws" 
        print(url)
        html = requests.get(url, headers={'user-agent': 'Mozilla/5.0'}).text
        soup = BeautifulSoup(html, 'html.parser')
        
        links = soup.find_all('a')
        
        
        earthquake = {}
        earthquake['actual_city'] = actual_city
        earthquake['occurence_timestamp'] = timestamp
        earthquake['occurence_date'] = day_month_year
        earthquake['magnitude'] = magnitude 
        news_articles = []
        earthquake['news'] = news_articles
        num_fails = 0
        for link in links:
            if 'google' not in link['href']:
                if ' ' in link.get_text():
                    print "Trying to fetch " 
                    print link['href']
                    #article = Article(link['href'], keep_article_html = True, request_timeout = 5)
                    article = Article(link['href'])
                    try:

                        print("Building %s" % (article.title))
                        article.download()
                        article.parse()
                        doc = {}
                        doc['title'] = article.title
                        doc['url'] = article.url
                        doc['content'] = article.text
                        print(article.publish_date)
                        #doc['html'] = article.html
                        news_articles.append(doc)
                        earthquake['news'] = news_articles
                        exit()
                    except:
                        print("Couldn't download article")
                        num_fails = num_fails + 1
                        #exit()

        #print urls
        return earthquake


#file_name = "earthquakes_world_2018_mag>=5_count=337.json"
file_name = "earthquakes_conterminousUS_2008-2018_mag>=4_count=1147.json"
file_without_ext = file_name.split(".")

output_file = "./News/News_" + file_without_ext[0] + ".json"
earthquake_data_json_path = "./UsgsData/" +file_name
crawler = news_crawler(earthquake_data_json_path, output_file)
crawler.crawl_news()

