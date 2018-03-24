from geopy.geocoders import Nominatim # install with pip3 install geopy
import re
import json

def read_earthquake_json(json_file, output_file):
    find_city_pattern = re.compile(r'.* of (.*)')

    # 1. First load from json
    data = json.load(open(json_file))
    features = data['features']
    for feature in features:
        properties = feature['properties']
        
        lon = feature['geometry']['coordinates'][0]
        lat = feature['geometry']['coordinates'][1]
        
        geolocator = Nominatim()
        place_nominatim = geolocator.reverse(str(lat)+ ","+str(lon))
        
        print("Place original " + properties['place'])
        print("Place nominatim " + place_nominatim.address)


#file_name = "earthquakes_conterminousUS_2008-2018_mag>=4_count=1147.json"
file_name = "earthquakes_world_2018_mag>=5_count=337.json"
file_without_ext = file_name.split(".")

output_file = "./Tweets/Tweets_" + file_without_ext[0] + ".json"
#earthquake_data_json_path = "./UsgsData/earthquakes_conterminousUS_2008-2018_mag>=4_count=1147.json"
earthquake_data_json_path = "./UsgsData/" +file_name
read_earthquake_json(earthquake_data_json_path, output_file)