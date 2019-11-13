import pytwits
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SentimentAnalyzer


## Scraping tweets from StockTwits with API authentication
tweets = []
tickers = []
access_token = '123456789'
stocktwits = pytwits.StockTwits(access_token=access_token) # This would also work without passing token.

def t_sentiment(comp):
    if comp > 0:
        return "Positive"
    elif comp < 0:
        return "Negative"
    else:
        return "Neutral"

def t_polarity(tweet):
    analyze = SentimentAnalyzer()
    return analyze.polarity_scores(tweet)['compound']


def GetTweetSentiment(stocks):
    for stock in stocks:
      symbol, cursor, messages = stocktwits.streams(path = 'symbol', id = stock) # set limit on messages by limit = __, max = 30)
      for msg in messages:
        tweets.append(msg.body)
        tickers.append(symbol.symbol)    

    tweet_df = pd.DataFrame({'Ticker': tickers, 'Tweet': tweets})

    #Sentiment scoring of tweets
    tweet_df['Tweet'] = tweet_df['Tweet'].str.replace("&#39;", "'")
    tweet_df['Tweet'] = tweet_df['Tweet'].str.replace("$", "")
    tweet_df['Tweet'] = tweet_df['Tweet'].str.replace('&quot;', '"')
    tweet_df['Tweet'] = tweet_df['Tweet'].str.replace("&amp;", "&")
    tweet_df['Score'] = tweet_df['Tweet'].apply(lambda x: t_polarity(x))       
    tweet_df['Sentiment'] = tweet_df['Score'].apply(lambda x: t_sentiment(x))
     
    return tweet_df
