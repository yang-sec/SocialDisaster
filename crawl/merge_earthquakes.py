import json
import re
import time
from math import sin, cos, radians, sqrt, pow , atan2

class merge_earthquake:
    
    def __init__(self, time_threshold_seconds, distance_threshold_km):
        self.sorted_by_timestamp = []
        self.final_list = []
        self.time_threshold_secs = time_threshold_seconds
        self.distance_threshold_km = distance_threshold_km
        
    def merge_file(self, file_name):
        
        print("Start merging file")
        #Iterate over the earthquake once:
        with open(file_name, 'r') as f:
            data = json.load(f)
            features = data['features']
            iteration = 0
            print("Number of earthquakes before merge " + str(len(features)))
            for feature in features:
                lon = feature['geometry']['coordinates'][0]
                lat = feature['geometry']['coordinates'][1]
                depth = feature['geometry']['coordinates'][2]
                timestamp = feature['properties']['time']
                id = feature['id']
                mag = feature['properties']['mag']
                self.sorted_by_timestamp.append([timestamp,lon,lat,depth, id,mag])
        
        self.sorted_by_timestamp.sort(key= lambda x: x[0])
        
        ids = {}
        already_processed = {}
        for i in range(0,len(self.sorted_by_timestamp)):
            earthquake = self.sorted_by_timestamp[i]
            
            # If already processed as part of previous cluster, skip.
            if already_processed.has_key(earthquake[4]):
                continue
                
            #for each earthquake, we check its neighbors until threshold is surpassed
            neighbor_earthquakes = []
            neighbor_earthquakes.append(earthquake)
            ts = earthquake[0]/1000
            for j in range(i+1, len(self.sorted_by_timestamp)):
                next_ts = self.sorted_by_timestamp[j][0]/1000
                if next_ts - ts > self.time_threshold_secs:
                    break
                    
                distance = self.get_distance(earthquake, self.sorted_by_timestamp[j])
                
                if distance < self.distance_threshold_km:
                    neighbor_earthquakes.append(self.sorted_by_timestamp[j])
            
            #now we sort "nearby" earthquakes by magnitude and pick best one
            neighbor_earthquakes.sort(key=lambda x: x[5]) #sorted ascending order
            best_id = neighbor_earthquakes[-1][4]
            ids[best_id] = True 
            
            # flag the cluster to avoid double processing
            for j in range(0,len(neighbor_earthquakes)):
                already_processed[neighbor_earthquakes[j][4]] = True
            
        
        # Now we just iterate again and pick the best earthquakes:
        final_earthquake_list = {}
        final_earthquake_list['features'] = []
        with open(file_name, 'r') as f:
            data = json.load(f)
            features = data['features']
            iteration = 0
            for feature in features:
                
                id = feature['id']
                
                if ids.has_key(id):
                    final_earthquake_list['features'].append(feature)

        print("Finish merging file")
        print("Number of earthquakes after merge " + str(len(ids.keys())))
        return final_earthquake_list
                
                
    
    def get_distance(self, e1, e2):
        # ref: stack overflow
        lon1 = radians(e1[1])
        lat1 = radians(e1[2])
        lon2 = radians(e2[1])
        lat2 = radians(e2[2])
        
        R = 6373 # Radius of earth in km
        
        # calculate curve on surface between two coordinates in rads
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = pow(sin(dlat / 2), 2) + cos(lat1) * cos(lat2) * pow(sin(dlon/2) ,2)
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        
        return distance