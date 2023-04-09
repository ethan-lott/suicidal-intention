import pandas as pd
from tqdm.notebook import tqdm
import snscrape.modules.twitter as sntwitter

# Scrape the most recent 50 tweets from the user 'twitter'
sntwitter.TwitterSearchScraper('from:twitter').get_items()

tweets = []

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
print(tweet_df.head())