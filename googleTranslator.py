from googleapiclient.discovery import build
import pickle
import json
import sys
import os

input_name = str(sys.argv[1])

# TRANSLATEEEE!!!!
def g_translate(source):
  # Create a server object
  service = build('translate', 'v2', developerKey='YOUR DEVELOPER KEY HERE')
  request = service.translations().list(q=source, target='en')
  response = request.execute()
  return response['translations'][0]['translatedText']

# Read in the data
tweets_data = []
tweets_file = open(input_name, "r")

for line in tweets_file:
  try:
    tweet = json.loads(line)
    tweets_data.append(tweet)
  except:
    continue

#sTranslate the tweets that are not in english
for tweet in tweets_data:
  if tweet['lang'] == 'en':
    continue
  else:
    translated = g_translate(tweet['text'])
    tweet['text'] = translated

# Store the data
filename, file_extension = os.path.splitext(input_name)
output_name = filename + '_translated.p'
with open(output_name, 'wb') as file:
  file.write(pickle.dumps(tweets_data))

print("Translations are now saved into %s." % (output_name))