import pickle, os, sys, csv, json

# Open the files
inputGeoJSON = None
with open('tweets_positive_weekend32.geojson') as f:
	inputGeoJSON = json.load(f)

ageDemographics = None
with open('tweets_positive_weekend32_demographics.json') as f_age:
	ageDemographics = json.load(f_age)

# Open the first name statistics
maleNames = []
with open('data/miestenNimet.csv', 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		maleNames.append(row)

femaleNames = []
with open('data/naistenNimet.csv', 'r') as ff:
	readerf = csv.reader(ff)
	for row in readerf:
		femaleNames.append(row)

males = 0;
females = 0;

# Compare and add the demographics
for tweet in inputGeoJSON['features']:

	# First the age group receivec from Demographics API by Applied-AI.nl
	for prediction in ageDemographics['response']['data']:
		if tweet['properties']['count'] == prediction['id']:
			tweet['properties']['age'] = prediction['age']

	# Then the comparison with first name statistics from Avoindata.fi
	# Split the names
	tweet['properties']['name'] = tweet['properties']['name'].split()
	userName = tweet['properties']['name'][0]
	for name in maleNames:
		possibleName = name[0]
		if userName == possibleName:
			tweet['properties']['gender'] = 'male'
			males = males + 1
			break
	for name_f in femaleNames:
		possibleName_f = name_f[0]
		if userName == possibleName_f:
			tweet['properties']['gender'] = 'female'
			females = females + 1
			break

# Save the updated GeoJSON file
with open('tweets_with_demographics.json', 'w') as fp:
	json.dump(inputGeoJSON, fp)

print(males)
print(females)