import json

# Data to be written
with open('json_data.json') as json_file:
    dictionary = json.load(json_file)
 
# Serializing json
json_object = json.dumps(dictionary, indent=10)

# Writing to sample.json
with open("sample.json", "w") as outfile:
	outfile.write(json_object)
