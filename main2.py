from stocktalk import streaming

# Credentials to access Twitter API 
API_KEY = 'XXXXXXXXXX'
API_SECRET = 'XXXXXXXXXX'
ACCESS_TOKEN = 'XXXXXXXXXX'
ACCESS_TOKEN_SECRET = 'XXXXXXXXXX'
credentials = [API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]

# First element must be ticker/name, proceeding elements are extra queries
TSLA = ['TSLA', 'Tesla']
SNAP = ['SNAP', 'Snapchat']
AAPL = ['AAPL', 'Apple']
AMZN = ['AMZN', 'Amazon']

# Variables
tickers = [TSLA,SNAP,AAPL,AMZN]  # Used for identification purposes
queries =  TSLA+SNAP+AAPL+AMZN   # Filters tweets containing one or more query 
refresh = 30                     # Process and log data every 30 seconds

# Create a folder to collect logs and temporary files
path = "/Users/Anthony/Desktop/Data/"

streaming(credentials, tickers, queries, refresh, path, \
realtime=True, logTracker=True, logTweets=True, logSentiment=True, debug=True)
