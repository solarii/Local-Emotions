import pickle, os, sys, csv, json

# The command line arguments
geojsonfile = str(sys.argv[1])
demographicsfile = str(sys.argv[2])

# Open the files
inputGeoJSON = None
with open(geojsonfile) as f:
	inputGeoJSON = json.load(f)

ageDemographics = None
with open(demographicsfile) as f_age:
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
with open(geojsonfile + '_demographics.geojson', 'w') as fp:
	json.dump(inputGeoJSON, fp)

print("Amount of males: %s" % males)
print("Amount of femals: %s" % females)
#print("Amount of unpredicted gender: %s" % ())