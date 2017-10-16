import requests
import json
import sys
import os

# Get the filename from command line arguments
inputFile = str(sys.argv[1])

# Open the data to be sent
with open(inputFile) as jsonFile:
	jsonData = json.load(jsonFile)

# Make the request to the Demographics API
# See more at: http://ai-applied.nl/api-documentation/2013/1/13/demographics-api-documentation

r = requests.post('http://api.ai-applied.nl/api/demographics_api/', data={"request": json.dumps(jsonData)})

# Save the response to a file
filename, fileExtension = os.path.splitext(inputFile)
with open(filename + '_demographics.json', 'wb') as fileToSave:
	fileToSave.write(r.content)