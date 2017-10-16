import requests
import json
import sys
import os

# Get the filename from command line arguments
#inputFile = str(sys.argv[1])
inputFile = 'twitterstream_weekend_translated_positive_demographics.json'

# Open the file
with open(inputFile) as jsonFile:
	jsonData = json.load(jsonFile)

# Arrays for demographics
females = []
males = [] 
unknown_gender = []

youth = []
youngAdults = []
adults = []
middleAged = []
retired = []



# Print it
for datum in jsonData['response']['data']:
	if datum['gender'] == 'female':
		females.append(datum)
	elif datum['gender'] == 'male':
		males.append(datum)
	elif datum['gender'] == 'unknown':
		unknown_gender.append(datum)
	if datum['age'] == '12-20':
		youth.append(datum)
	elif datum['age'] == '21-30':
		youngAdults.append(datum)
	elif datum['age'] == '31-40':
		adults.append(datum)
	elif datum['age'] == '41-55':
		middleAged.append(datum)
	elif datum['age'] == '56-65':
		retired.append(datum)


print('Females: %d' % len(females))
print('Males: %d' % len(males))
print('Unknown: %d' % len(unknown_gender))

print('12-20: %d' % len(youth))
print('21-30: %d' % len(youngAdults))
print('31-40: %d' % len(adults))
print('41-55: %d' % len(middleAged))
print('51-65: %d' % len(retired))