## Processing the raw data in .json files
## Fetch tweets
import json
from pprint import pprint
import datetime
import time
from helperFunctions import monthName


# Read .json files
data = json.load(open('./UsgsData/earthquakes_world_2018_mag>=5_count=337.json'))

for i in range(10):
	eqk_mag = data["features"][i]["properties"]["mag"]

	eqk_time = data["features"][i]["properties"]["time"]

	eqk_place = data["features"][i]["properties"]["place"]

	eqk_date = datetime.date.fromtimestamp(int(eqk_time/1000))

	print('Mag:',eqk_mag,eqk_place,monthName(eqk_date.month),eqk_date.day,eqk_date.year)


# Search and store tweets


# Store the earthquake information that will be used for training TW