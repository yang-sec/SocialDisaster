## Processing the raw data in .json files
import json
from pprint import pprint
import datetime

# Read .json files
#data = json.load(open('./UsgsData/earthquakes_world_2018_mag>=5_count=337.json'))
data = json.load(open('./UsgsData/testfile_count=6.json'))

eqk_mag = data["features"][0]["properties"]["mag"]
pprint(eqk_mag)

eqk_time = data["features"][0]["properties"]["time"]
pprint(eqk_time)

eqk_datetime = datetime.datetime.fromtimestamp(int(eqk_time/1000)).strftime('%Y-%m-%d %H:%M:%S')
print(eqk_datetime)


# Store the earthquake information that will be used for training TW