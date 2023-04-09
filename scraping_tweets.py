import pandas as pd
import numpy as np
import re
from tqdm.notebook import tqdm
import snscrape.modules.twitter as sntwitter

# Scrape the most recent 50 tweets from the user 'twitter'
sntwitter.TwitterSearchScraper('from:twitter').get_items()

tweets = []
handle 

for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:fabrizioromano').get_items()):
    data = [
        tweet.date,
        tweet.id,
        tweet.content,
        tweet.user.username,
        tweet.user.displayname,
        tweet.user.description,
        tweet.user.location,
        tweet.user.followersCount,
        tweet.user.friendsCount,
        tweet.user.verified
    ]
    tweets.append(data)
    if i>50:
        break

tweet_df = pd.DataFrame(tweets, columns=['Datetime', 'Tweet Id', 'Text', 'Username', 'Display Name', 'Bio', 'Location', 'Followers', 'Following', 'Verified'])
recent_tweets = np.array(tweet_df['Text'])

escapes = ''.join([chr(char) for char in range(1, 32)])
translator = str.maketrans('', '', escapes)

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)

for i in range(len(recent_tweets)):
    tweet = recent_tweets[i]
    if 'http' in tweet:
        tweet = (tweet)[0:tweet.find('http')]
    tweet = tweet.translate(translator)
    tweet = emoji_pattern.sub(r'', tweet)
    recent_tweets[i] = tweet

print(recent_tweets)