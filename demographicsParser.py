import json
import sys
import os

# Open the data file 
inputFile = sys.argv[1]
data = None
with open(inputFile, 'r') as f:
	data = json.load(f)

# Parse the JSON file
# The template for Demographics API
# Check more at http://ai-applied.nl/demographics-api/
template = \
'''
				{
				"text": "%s",
				"language_iso": "eng",
				"user": "%s",
				"id": %d
				},
'''

# The head of the json file
output =  \
    ''' \
{ 
   "data": {
   		"api_key": "YOUR API KEY HERE",
   		"call": {
   			"return_original": true,
   			"data":[
	'''

i = 0

# Loop trough the raw data
for datum in data['features']:
	text = datum['properties']['text'].replace('\\', '').replace('"','\\"').replace('\n', '')
	user = datum['properties']['screen_name']
	idN = datum['properties']['count']
	output += template % (text, user, idN)

# The tail of the json file
output += \
    ''' \
	    	]
		}
	}
}
    '''
    
# Save the file
filename, fileExtension = os.path.splitext(inputFile)
with open(filename + '.json', 'w') as outputFile:
	outputFile.write(output)

