Sentiment analysis and heatmap visualization for geolocated tweets
==================

This project was made as a part of research project for Aalto university's Ambient Intelligence Research Team. You can learn more about the team and our work at: http://ambientintelligence.aalto.fi/

With this application you can crawl for tweets with your preferred searchterms (keywords, locations, users etc.), do an sentiment analyzation for them (positive, negative or neutral opinion), and then visualize them as a heatmap based on their location.

Required installations
------------------

You need to have your system running Python 3.x and install some required libraries.

	pip3 install tweepy
	pip3 install vader
	pip3 install folium

How to use
-----------------

The workflow happens in three parts:

1. Crawl the tweets from Streaming API
2. Translate the tweets
3. Analyze the tweets for sentiment and draw the map

For added things, like demographigs and time animation you can also do the following:

4. Analyze the tweets for demographis
5. Parse it all together to a geoJSON-file
6. Visualize the geoJSON file in browser


Twitter Streaming API
-----------------

You first need to crawl for tweets using Twitter's Streaming API.

In "twitterStreamingAPI.py" specify what do you want to search for. The default is looking for tweets in the area surrounding Helsinki. 
For more info on the search parameters, check out Twitter's official documentation (https://dev.twitter.com/streaming/overview/request-parameters) 
and the tweepy library (http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html).

You need to have login credentials for Twitter before running the script. Get your own credentials from: https://dev.twitter.com/.

After you have done that and updated the code ***with your API keys***, run the code with

	python3 twittersStreamingAPI.py > tweets.txt

Now the tweets will saved onto the file names "tweets.txt".


Google Translate
-----------------

Because our tweets contain non-english language we have translate them with Google Cloud's Translate API. Note, that you need your own API credentials for this. The service is also a freemium model, where you're given 300 euros worth of credit to test the service with. After this it will cost $20 per million characters.

To register an account with free credit, visit https://cloud.google.com/translate/.

After this, update the field in "googleTranslator.py" with your developer key. Then you can run the translation with:

	python3 googleTranslator.py tweets.txt

It might take a while, depending on the size of your text file (so don't rush). If everything goes right you should see:

	"Translations are now saved into tweets_translated.p"


Sentiment analysis
-----------------

Sentiment analysis uses the awesome VADER library built for python. It is a lexicon and rule-based sentiment analysis tool that is made specifically for social media text. It is very light and accurate.

https://github.com/cjhutto/vaderSentiment

To perform the sentiment analysis, run:

	python3 sentimentAnalyzer.py tweets_translated.p map.html

It will analyze the tweets and draw a folium map with heatmap visualization named "map.html". In addition two pickle-files "tweets_translated_negative.p" and "tweets_translated_positive.p" are produced.

