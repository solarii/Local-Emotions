# Imports
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Variables for twitter authentication
# Replace with your tokens
# To get tokens, visit: https://dev.twitter.com/oauth
access_token = "166265377-rH2Q2VOXXepf2WdCOXJgCwlX1TKQjU60xoAPX7lZ"
access_token_secret = "IoSgfjbor93qE91amdFj4Ddjt3BqVM2Rkzr6VY3NqHITb"
consumer_key =  "48yGd5NJFsm47zkPjZoIJudJq"
consumer_secret = "WsPrCQdJURk2RA61Gp4P5ackH1Z5q5MGFLNM9d77es47GKsSbc"

# The listener that prints out the tweets
# If you want to save them into a file, and not just print on the screen use "python3 twitterstream.py > filetosave.txt" when running the script
class StdOutListener(StreamListener):

	def on_data(self, data):
		print(data)
		return True

	def on_error(self, status):
		print(status)

	def on_timeout(self):
		print('Timeout...')
		return True # don't kill the stream

# Checks the modules and everything before executing the script
if __name__ == '__main__':

	# This handles the Twitter Authentication and the connection to Twitter's Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)

	# This line filters our stream
	# You can specify here what do you want to stream (location, keywords etc)
	# Now we are looking for tweets around the Helsinki metropolitan area
	# For more specifications, see https://dev.twitter.com/streaming/overview/request-parameters
	stream.filter(locations=[24.6,60.1,25.2,60.3])