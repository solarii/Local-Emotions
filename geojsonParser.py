import pickle
import sys
import os

# Get the name of the file to convert
inputName = str(sys.argv[1])

# Read the data
rawData = pickle.load( open( inputName, "rb"))

# The template for the geoson
template = \
	''' \
   { "type" : "Feature",
		"geometry" : {
			"type" : "Point",
			"coordinates" : %s
		},
		"properties" : {
			"id" : %s,
			"count": %d,
			"screen_name": "%s",
			"name": "%s",
			"text": "%s",
			"sentiment_score" : %s,
			"time" : "%s",
			"gender": null,
			"age": null
			}
		},
	'''

# The head of the geojson file
output = \
	''' \
{ "type" : "FeatureCollection",
	"features" : [
	'''

i = 0
# Loop trough the raw data
for datum in rawData:
	if datum['coordinates'] is not None:
		idN = datum['id']
		coordinates = datum['coordinates']['coordinates']
		text = datum['text'].replace('\\', '').replace('"','\\"').replace('\n', '')
		screen_name = datum['user']['screen_name']
		name = datum['user']['name']
		sentiment_score = datum['sentiment_score']['compound']
		time = datum['created_at']
		i = i + 1
		output += template % (coordinates, idN, i, screen_name, name, text, sentiment_score, time)

# The tail of the geojson file
output += \
	''' \
	]
}
	'''
	
# Save the file
filename, file_extension = os.path.splitext(inputName)
with open(filename + '.geojson', 'w') as outputFile:
	outputFile.write(output)