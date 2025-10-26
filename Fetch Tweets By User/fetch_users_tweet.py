'''
Using Twitter API, fetch all tweets posted by a particular Twitter handle
Here I am fetching all tweets by @MumbaiPolice on lockdown

helped API DOC

https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
'''


#access token = "Jt350086556-OHeT0fMKHeVSknIyMZNpXlDEFQGLj149Yiazia"
#access token secret = "eWFjDcwDsfV7I4iYvhnG8ozgi7VHDM8vcXsovYJprRchj"

import os
from requests_oauthlib import OAuth1Session
import json


consumer_key = 'Your consumer key'
consumer_secret = 'Your secret key'


# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
fetch_response = oauth.fetch_request_token(request_token_url)
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')
print("Got OAuth token: %s" % resource_owner_key)

# # Get authorization
base_authorization_url = 'https://api.twitter.com/oauth/authorize'
authorization_url = oauth.authorization_url(base_authorization_url)
print('Please go here and authorize: %s' % authorization_url)
verifier = input('Paste the PIN here: ')

print('controller reached here>>>>>>>>>>>>>>')
# # Get the access token
access_token_url = 'https://api.twitter.com/oauth/access_token'
oauth = OAuth1Session(consumer_key,
                     client_secret=consumer_secret,
                     resource_owner_key=resource_owner_key,
                     resource_owner_secret=resource_owner_secret,
                     verifier=verifier)
oauth_tokens = oauth.fetch_access_token(access_token_url)

# print('controller reached here>>>>>>>>>>>>>>')


access_token = oauth_tokens['oauth_token']
access_token_secret = oauth_tokens['oauth_token_secret']

params = {"screen_name": "MumbaiPolice", 'count':'200'}


# Make the request
oauth = OAuth1Session(consumer_key,
                       client_secret=consumer_secret,
                       resource_owner_key=access_token,
                       resource_owner_secret=access_token_secret)

response = oauth.get("https://api.twitter.com/1.1/statuses/user_timeline.json", params = params)

# response = oauth.get("https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=MumbaiPolice&since_id=1249248288433246210")

print("Response status: %s" % response.status_code)
# print("Body: %s" % response.text)

j_response = json.loads(response.text)
# print("response>>>>>>>",j_response,)
for text in j_response:
    ans = text.get('text')
    print(ans)

