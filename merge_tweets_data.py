import os
import json

working_dir = os.path.dirname(os.path.realpath(__file__))
list_files = []
obj = {}
for subdir, dirs, files in os.walk(working_dir + "/Tweets"):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file


        if file.endswith(".json"):
            #print filepath
            if not "crawler" in filepath and not "merged" in filepath:
                list_files.append(filepath)
                print (filepath)


merged_json = None
for file in list_files:
    # Open the json
    with open(file, 'r') as f:
        data = json.load(f)
        print("Number of earthquakes " + str(len(data)))
        # 2 save it in a dictionary
        if merged_json is None:
            merged_json = data
        else:
            merged_json.extend(data)




# 3 save dict.

output_file_name = "Tweets" + os.sep + "Tweets_earthquakes_merged_2008-2018_count=20470.json"
with open(output_file_name, 'wb') as outfile:
    json.dump(merged_json, outfile, indent=4, sort_keys=True)
    print "total earthquakes " + str(len(merged_json))
    print output_file_name