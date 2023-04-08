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

# inputs = ["I feel alright.", "I feel neither good nor bad.", "Whatever.", "Goodbye cruel world", "Living life to the fullest!"]

flags = []
no_flags = []

for entry in df_array:
    if entry[1] == 1:
         flags.append(entry[0])
    else:
         no_flags.append(entry[0])

print(len(flags))
print(len(no_flags))

outputs = []

for input in df_text[0:10]:
    output = query({"inputs": input})
    print(output)