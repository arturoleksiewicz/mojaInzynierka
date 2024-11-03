import tweepy
import pandas as pd

consumer_key = "QU5xMHFMcUtWd2JnQVJXbnFMV2w6MTpjaQ" #Your API/Consumer key
consumer_secret = "2xuPEVPAFwPI9_UuUwAK75mOStm2rcUejP2D-eV4XemCDobg-g" #Your API/Consumer Secret Key
access_token = "1754626067589992448-bqdWABeKjaHfDoFh7C2bq7hbPXG8sk"    #Your Access token key
access_token_secret = "ZgbYdsOKEgctgg4RWwOj9jUkInOUeMRSuyFSCNV7IflQo" #Your Access token Secret key

# Pass in our twitter API authentication key
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Instantiate the tweepy API
api = tweepy.API(auth, wait_on_rate_limit=True)

search_query = "Tesla -filter:retweets AND -filter:replies AND -filter:links"
no_of_tweets = 100

try:
    # The number of tweets we want to retrieve from the search
    tweets = api.search_tweets(q=search_query, lang="en", count=no_of_tweets, tweet_mode='extended')

    # Pulling Some attributes from the tweet
    attributes_container = [[tweet.user.name, tweet.created_at, tweet.favorite_count, tweet.source, tweet.full_text] for
                            tweet in tweets]

    # Creation of column list to rename the columns in the dataframe
    columns = ["User", "Date Created", "Number of Likes", "Source of Tweet", "Tweet"]

    # Creation of Dataframe
    tweets_df = pd.DataFrame(attributes_container, columns=columns)

    # Save to CSV
    tweets_df.to_csv('tesla_tweets.csv', index=False)

    print(f"Successfully saved {len(tweets_df)} tweets to tesla_tweets.csv")

except tweepy.TweepError as e:
    print('Status Failed On,', str(e))
