print("NLP Based News Articler Recommender")

#import libraries
import seaborn as sns
import matplotlib as plt
import bs4 as bs
import csv
import requests
import urllib
from urllib.request import urlopen
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
from datetime import date, timedelta
from datetime import datetime
from dateutil import parser
from IPython.display import HTML
import configparser
import ast
import StockMovement
import WSJScraper
import YahooFinScraper
import ReutersScraper
import Relevancy
import SentimentScoring
import Dashboard
import StockTwits

#Start time and Configuration
starttime = datetime.now()
print('StartTime : ')
print(starttime)
config = configparser.RawConfigParser()
config.read('Configuration.cfg')


# Number of Days to look at
num_of_days_str = config["DEFAULT"]["num_of_days"]
num_of_days = (int)(num_of_days_str)
last_date = date.today() - timedelta(days=(num_of_days-1))

#Scraping
AllArticles = []
cols=['Ticker','Date','Title','Link','Text']
df_articles = pd.DataFrame([],columns=cols)
tickerlist = config["DEFAULT"]["ticker_list"]
stocks = ast.literal_eval(tickerlist)
print(stocks)

print("-----------Scraping WSJ Articles------------")
wsjarticles, AllArticles1 = WSJScraper.GetArticles(stocks, last_date)
print("Count of WSJ Articles:")
print(len(wsjarticles))


print("-----------Scraping YahooFin Articles------------")
yahoofinarticles, AllArticles2 = YahooFinScraper.GetArticles(stocks, last_date)
print("Count Of YahooFin Articles:")
print(len(yahoofinarticles))

print("-----------Scraping Reuters Articles------------")
reuters_articles, AllArticles3 = ReutersScraper.GetArticles(stocks, last_date)
print("Count Of Reuters Articles:")
print(len(reuters_articles))

# Articles from all scrapers
AllArticles = AllArticles1 + AllArticles2 + AllArticles3
df_articles = pd.concat([wsjarticles, yahoofinarticles, reuters_articles])

#Create CSV
filename = 'AllArticlesOutput'+ datetime.now().strftime('%Y-%m-%d-%H-%M') +'.csv'
with open(filename,'w', newline='') as resultFile:
    wr = csv.writer(resultFile)
    wr.writerow(['Ticker','Date','Title','Link','Text'])
    # Write Data to File
    for item in AllArticles:
       try:
          wr.writerow(item)
       except:           
          continue

#Relevancy
df_unique = Relevancy.RemoveDuplicates(stocks, df_articles)
endtime = datetime.now()
print('EndTime After Relevancy : ')
print(endtime)

# sentiment scoring
df_unique = SentimentScoring.ScoreArticles(df_unique)
endtime = datetime.now()
print('EndTime after Sentiment scoring: ')
print(endtime)

# tweet sentiment scoring
tweet_df = StockTwits.GetTweetSentiment(stocks)
endtime = datetime.now()
print('EndTime after Sentiment scoring: ')
print(endtime)

#Dashboard
df_unique['Score'] = df_unique['Score'].apply(lambda x: round(x,2))
Dashboard.CreateDashboardWithTweets(stocks, df_unique, tweet_df)
endtime = datetime.now()
print('EndTime after creating Dashboard: ')
print(endtime)
