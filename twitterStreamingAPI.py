# Imports
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Variables for twitter authentication
# Replace with your tokens
# To get tokens, visit: https://dev.twitter.com/oauth
access_token = "YOUR TOKEN HERE"
access_token_secret = "YOUR SECRET HERE"
consumer_key =  "YOUR TOKEN HERE"
consumer_secret = "YOUR SECRET HERE"

# The listener that prints out the tweets
# If you want to save them into a file, and not just print on the screen use "python3 twitterstream.py > filetosave.txt" when running the script
class StdOutListener(StreamListener):

	# Prints out the received data, run "python3 twitterStreaminAPI.py > tweets.txt" to save them into a file
	def on_data(self, data):
		print(data)
		return True

	# Print errors
	def on_error(self, status):
		print(status)

	# Don't worry about timeouts
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