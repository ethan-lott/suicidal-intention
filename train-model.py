import pandas as pd
import numpy as np
import requests

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

n = 50
sum_flags = 0

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

avg_flags = sum_flags / n
avg_no_flags = sum_no_flags / n

print(avg_flags)
print(avg_no_flags)