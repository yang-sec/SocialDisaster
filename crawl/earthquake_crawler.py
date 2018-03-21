#!/usr/bin/python
import pprint, json, urllib2
import smtplib

#Size is the number of days worth of data
def getUSGS_json(size):
    print "Fetch data from URL"

    fileName = 'earthquakes_'+str(size)+'days.json'
    url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson'

    try:
        urllib2.urlopen(url)
        filePut = open(fileName, 'w')
        data = urllib2.urlopen(url).read()

    except urllib2.HTTPError, e:
        print(e.code)

        emailNotify(e.code, url)
        data = 0
    except urllib2.URLError, e:
        print(e.args)

        emailNotify(e.args, url)
        data = 0

    if data != 0:  # validate url
        try:
            with open(fileName) as jsonGetData:
                # add data
                filePut.write(data)
                filePut.close()

                j = json.load(jsonGetData)
                print "Json processed."
                return 1
        except Exception, e:
            print e
            emailNotify(e, url)

            raise
        else:
            pass
        finally:
            pass
    else:
        print url, " Not available."
        return 0


# end getUSGS_json

def returnJson(source):
	#Grab destination file json
	try:
	   with open(source) as jsonFile: # Open and verify file is there
	   	# load JSON object into memory
		j = json.load(jsonFile)

		return j
	except Exception, e:
		print e
		raise
# end returnJson


getUSGS_json(7)
