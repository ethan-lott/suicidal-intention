from twython import Twython, TwythonError
import requests

CONSUMER_KEY = 'X7tnd3NyWl6f1BfzIzItgMVIa'
CONSUMER_SECRET = 'Cx9yYNO3X3q2FLfl9ujGAwYeq1KZnCQMLnL67WkAR4r7G995QW'

ACCESS_TOKEN = '1644799506276401152-sGBhRCgm48dfze4H2ilhDLaOYn9x5J'
ACCESS_TOKEN_SECRET = 'FOqWDQG64q2HQMM9SlIjcf2fMjzkBv71CxsMaGVbcBA5P'

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAKNfmgEAAAAAFyIws4nm0rhY66HsF7bbETGMDTQ%3Dxi6MBCvc47AHJt2tB4zseYKxZKwixxSGCatdo9QokW8e5pmOhl'

OAUTH_TOKEN = 'dHVDdG1iVHRFZFdQMGFPcjdITmo6MTpjaQ'
OAUTH_TOKEN_SECRET = 'fMH09MfB_aGfFS-VmBeo06w2bGWm6rCAcWyKMenhv-kl4WvFfU'

headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}

twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET)

username = 'wellness_nudge'

try:
    response = requests.get(f'https://api.twitter.com/2/users/by/username/{username}', headers=headers)
    user_info = response.json()
except TwythonError as e:
    print(e)

print(user_info)
