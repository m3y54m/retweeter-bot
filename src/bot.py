import os
import tweepy
from dotenv import load_dotenv

# take environment variables from .env.
load_dotenv()

# get environment variables for Twitter API
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
bearer_token = os.environ.get("BEARER_TOKEN")


def twitter_api_authenticate():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
    except Exception as error:
        print(
            f"\n[ SimJowBot ] An error occurred while attempting to authenticate with the twitter API. Reason:\n{error}"
        )
        return None
    else:
        return api


def get_tweet(twitterApi, tweetId):
    userName = None
    tweetText = None

    if twitterApi:
        try:
            status = twitterApi.get_status(id=tweetId)
        except Exception as error:
            print(
                f"\n[ SimJowBot ] An error occurred while attempting to get the twitter status with id={tweetId}. Reason:\n{error}"
            )
        else:
            userName = status.user.name
            tweetText = status.text

    return userName, tweetText


def post_tweet(twitterApi, tweetText):
    success = False

    if twitterApi:
        try:
            twitterApi.update_status(status=tweetText)
        except Exception as error:
            print(
                f"\n[ SimJowBot ] An error occurred while attempting to update the twitter status. Reason:\n{error}"
            )
        else:
            success = True

    return success


# public_tweets = api.home_timeline()

# with open('timeline.txt', 'w') as f:
#     for tweet in public_tweets:
#         f.write(tweet.text + "\r\n")

if __name__ == "__main__":
    pass
    # username, text = get_tweet_text(20)
    # print(f"{username}: {text}")

    # print(get_timeline())
