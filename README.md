Sentiment analysis and heatmap visualization for geolocated tweets
==================

This project was made as a part of summer research project for Aalto university's Ambient Intelligence Research Team. You can learn more about the team and our work at: http://ambientintelligence.aalto.fi/

With this application you can crawl for tweets with your preferred searchterms (keywords, locations, users etc.), do an sentiment analyzation for them (positive, negative or neutral opinion), and then visualize them as a heatmap based on their location.

Required installations
------------------

You need to have your system running Python 3.x and install some required libraries.

	pip3 install tweepy
	pip3 install vader
	pip3 install folium

How to use
-----------------

You first need to crawl for tweets using Twitter's Streaming API.

In "twitterStreamingAPI.py" specify what do you want to search for. The default is looking for tweets in the area surrounding Helsinki. 
For more info on the search parameters, check out Twitter's official documentation (https://dev.twitter.com/streaming/overview/request-parameters) 
and the tweepy library (http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html).

You need to have login credentials for Twitter before running the script. Get your own credentials from: https://dev.twitter.com/.

After you have done that and updated the code ***with your API keys***, run the code with
	python3 twittersStreamingAPI.py > tweets.txd

Sentiment analysis
-----------------

Sentiment analysis uses the awesome VADER library built for python. It is a lexicon and rule-based sentiment analysis tool that is made specifically for social media text. It is very light and accurate.

https://github.com/cjhutto/vaderSentiment