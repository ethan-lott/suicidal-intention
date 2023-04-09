import pandas as pd
import numpy as np
import re
from tqdm.notebook import tqdm
import snscrape.modules.twitter as sntwitter
import requests
import math
import tensorflow as tf
import pickle
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.sequence import pad_sequences

def query(payload, API_URL, headers):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def scrape_tweets(twit_handle, NUM_TWEETS):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{twit_handle}').get_items()):
        data = [tweet.rawContent]
        tweets.append(data)
        if i>NUM_TWEETS:
            break
    tweet_df = pd.DataFrame(tweets, columns=['Text'])
    recent_tweets = np.array(tweet_df['Text'])
    return recent_tweets

def clean_tweets(tweets):
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
    for i in range(len(tweets)):
        tweet = tweets[i]
        if 'http' in tweet:
            tweet = (tweet)[0:tweet.find('http')]
        tweet = tweet.translate(translator)
        tweet = emoji_pattern.sub(r'', tweet)
        tweets[i] = tweet
    return tweets

def calculate_score(tweets, API_URL, headers, NUM_TWEETS):
    num_used = NUM_TWEETS
    suicide_score = 0
    for tweet in tweets:
        if len(tweet) < 10:
            num_used -= 1
        else:
            tweet_check = query({"inputs": tweet}, API_URL, headers)[0]
            if tweet_check[0]['label'] == "NEGATIVE" and tweet_check[0]['score'] > 0.85:
                suicide_score += 1

    suicide_score /= num_used
    return suicide_score

def convert_text_to_sequences(text):
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
        sequences = tokenizer.texts_to_sequences(text)
        padded = pad_sequences(sequences, maxlen=100, padding='post', truncating='post')
        return padded

def predict_score(tweets, NUM_TWEETS, model):
    THRESHOLD = 0.85
    predictions = []
    num_used = NUM_TWEETS
    for tweet in tweets:
        if len(tweet) < 10:
            num_used -= 1
        else:
            sequences = convert_text_to_sequences([tweet])
            prediction = model.predict(sequences)
            predictions.append(prediction[0][1])

    predictions = np.array(predictions)
    if any(x > THRESHOLD for x in predictions):
        larger = predictions[predictions > 0.5]
        return sum(larger)/len(larger)
    else:
        return sum(predictions)/len(predictions)

def main(twit_handle, NUM_TWEETS):
    # API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
    # API_TOKEN = "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"
    # headers = {"Authorization": f"Bearer {API_TOKEN}"}
    # twit_handle = 'proclubwhitetee'

    recent_tweets = scrape_tweets(twit_handle, NUM_TWEETS)
    recent_tweets = clean_tweets(recent_tweets)
    # suicide_score = calculate_score(recent_tweets, API_URL, headers, NUM_TWEETS)
    model = keras.models.load_model('twitter-suicidal_model')
    suicide_score = predict_score(recent_tweets, NUM_TWEETS, model)

    return suicide_score