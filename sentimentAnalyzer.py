import pickle
import folium
import json
import numpy as np
import sys
import os
from folium.plugins import HeatMap
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

input_name = str(sys.argv[1])
output_name = str(sys.argv[2])

tweets_data = pickle.load( open( input_name, "rb"))

# VADER: Sentiment Analysis
analyzer = SentimentIntensityAnalyzer()
for tweet in tweets_data:
    vs = analyzer.polarity_scores(tweet['text'])
    # Add the score to the tweets dictionary
    tweet['sentiment_score'] = vs

# Separate the negative and positive tweets
positive_tweets = []
negative_tweets = []
for tweet in tweets_data:
	if tweet['sentiment_score']['compound'] > 0:
		positive_tweets.append(tweet)
	elif tweet['sentiment_score']['compound'] < 0:
		negative_tweets.append(tweet)

# Save the tweets
filename, file_extension = os.path.splitext(input_name)
positive_tweets_file = filename + "_positive.p"
negative_tweets_file = filename + "_negative.p"
with open(positive_tweets_file, 'wb') as posfile:
	posfile.write(pickle.dumps(positive_tweets))
with open(negative_tweets_file, 'wb') as negfile:
	negfile.write(pickle.dumps(negative_tweets))

# The Map - change for your own coordinates!
map_osm = folium.Map(location=[60.1699, 24.9348], zoom_start=12)

# HeatMap
coordinates_pos = []
coordinates_neg = []

for tweet in positive_tweets:
	try:
		coordinates_pos.append(tweet['coordinates']['coordinates'])
	except:
		continue

for tweet in negative_tweets:
	try:
		coordinates_neg.append(tweet['coordinates']['coordinates'])
	except:
		continue

# Reverse the coordinates (god damn GeoJSON!)
for c in coordinates_pos:
	c.reverse()
for c in coordinates_neg:
	c.reverse()


map_osm.add_child(HeatMap(coordinates_pos))
map_osm.add_child(HeatMap(coordinates_neg))

# Save the map for display
folium.LayerControl().add_to(map_osm)
map_osm.save(output_name)

print('Positive geolocated tweets: %d' % len(coordinates_pos))
print('Negative geolocated tweets: %d' % len(coordinates_neg))
print('Map %s is now ready.' % (output_name))