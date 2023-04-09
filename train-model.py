import pandas as pd
import numpy as np
import requests
import math

API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
API_TOKEN = "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"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

df = pd.read_csv(r'twitter-suicidal_data.csv')
df_array = np.array(df)
# print(df_text)

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

flags = []
no_flags = []

for entry in df_array:
    if entry[1] == 1:
         flags.append(entry[0])
    else:
         no_flags.append(entry[0])

n = 150
sum_flags = 0
'''
for flag in flags[0:n]:
    flag_output = query({"inputs": flag})[0]
    if flag_output[0]['label'] == 'NEGATIVE':
        sum_flags += 1
'''
sum_no_flags = 0

for no_flag in no_flags[600:600+n]:
    no_flag_output = query({"inputs": no_flag})[0]
    if no_flag_output[0]['label'] == 'POSITIVE':
        sum_no_flags += no_flag_output[0]['score']
    else:
        sum_no_flags += no_flag_output[1]['score']

'''
for flag in flags[0:50]:
    flag_output = query({"inputs": flag})[0]
    if flag_output[0]['label'] == 'NEGATIVE':
        sum_flags += flag_output[0]['score']
    else:
        sum_flags += flag_output[1]['score']
    print("FLAGGED: ", flag_output[0], '\t', flag_output[1])

sum_no_flags = 0

for no_flag in no_flags[0:50]:
    no_flag_output = query({"inputs": no_flag})[0]
    if no_flag_output[0]['label'] == 'POSITIVE':
         sum_no_flags += no_flag_output[0]['score']
    else:
        sum_no_flags += no_flag_output[1]['score']
    print("NOT FLAGGED: ", no_flag_output[0], '\t', no_flag_output[1])
'''
# avg_flags = sum_flags / n
avg_no_flags = sum_no_flags / n

# print(avg_flags)
print(avg_no_flags)

# avg(0:150) = 0.1533027401183305
# avg(150:300) = 0.18056777726655127
# avg(300:450) = 0.13488133024259394
# avg(450:600) = 0.2010578573733801
# avg(600:750) = 

for tweet in recent_tweets:
     tweet_check = query({"inputs": tweet})[0]
     print(tweet_check)