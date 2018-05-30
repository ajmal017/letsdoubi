import tweepy

consumer_key = 'duXvAgTq4VdLcL2iEi539krNQ'
consumer_secret = 'FjZlUXWqeIDLIa02oAgdRZuln6ErQtY1cRWNcZZfkstbdjBTh0'
access_token = '1025683382-AqdI8Wm115vQXhhXz02Lrpg9Xrh9hxAguRryaLX'
access_token_secret = '3jmSNxSCtUmEJ8VmWRRY9iCuOCFze35Epu48L8ssxDNcv'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


for status in tweepy.Cursor(api.search,
                            q='gtx 1080',
                            include_entities=True,
                            lang="en").items(10):
    print(status.user.followers_count)
    print(status.id)
    print(status.text)
    print(status.favorite_count)
    print(status.created_at)
    print(status.retweet_count)