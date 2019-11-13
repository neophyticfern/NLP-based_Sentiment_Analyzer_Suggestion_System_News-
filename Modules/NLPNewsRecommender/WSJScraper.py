import bs4 as bs
import csv
import requests
import urllib
import re
from urllib.request import urlopen
import Common
from datetime import date, timedelta
from datetime import datetime
from dateutil import parser
import pandas as pd

def GetWSJContent(article_link):  
    strContent=''
    url = article_link
     #print(url)
 
    #req = urllib.request.Request(url, headers={'User-Agent': 'IE9'})
    with urllib.request.urlopen(url) as f:
        #sourcehtml = urlopen(req)
        #print(sourcehtml)
        soup = bs.BeautifulSoup(f.read().decode('utf-8'),"lxml")        
        #print(soup)
        
        if url.find("marketwatch") != -1:
            BulletsDiv = soup.find("div", {"id": "article-body"})
            if BulletsDiv is not None:
               pbullets = BulletsDiv.findAll("p")
               for bullet in pbullets:
                  bulletHolder = bullet.get_text().strip() 
                  strContent = strContent + bulletHolder  
                  strContent = strContent.replace("\r","")
                  strContent = strContent.replace("\n","")
                  strContent = strContent.replace('  ', ' ')
                  re.sub(' +', ' ',strContent)
        elif url.find("barrons") != -1 :
            BulletsDiv = soup.find("div", {"itemprop": "articleBody"})
            if BulletsDiv is not None:
               pbullets = BulletsDiv.findAll("p")
               for bullet in pbullets:
                  bulletHolder = bullet.get_text().strip() 
                  strContent = strContent + bulletHolder  
                  strContent = strContent.replace("\r","")
                  strContent = strContent.replace("\n","")
                  strContent = strContent.replace('  ', ' ')
                  re.sub(' +', ' ',strContent)
                
    return strContent  

#------------ Wall Street Journal News Parser-------------

def GetArticles(stocks, last_date):
    cols=['Ticker','Date','Title','Link','Text']
    df_articles = pd.DataFrame([],columns=cols)   
    AllArticles = []
    for stock in stocks :
       url = "https://quotes.wsj.com/"+stock
       print(url)
       req = urllib.request.Request(url, headers={'User-Agent' : "foobar"})
       sourcehtml = urlopen(req)
       soup = bs.BeautifulSoup(sourcehtml.read().decode('utf-8'),"lxml")  

       #Parse the document using soup object and extract the required text 
       mydivs = soup.findAll("span", {"class":"headline"}) 
       mydiv_time = soup.findAll("li", {"class":"cr_dateStamp"})
    
       mydiv_url = soup.findAll("span", {"class":"headline"})
    
       print("-----------"+stock+"------------")

       for i,div in enumerate(mydivs):       
            atextHolder = div.findAll('a')
            articleHolder = atextHolder[0].get_text().strip()
            article_url = mydiv_url[i].find('a').attrs['href']
            article_time = mydiv_time[i].get_text()
            article_FormattedDate  = Common.ConvertDate(article_time)   

            try:
               article_date = parser.parse(article_FormattedDate)
            except:           
               article_date = datetime.now()

            if  article_date.date() < last_date :
                break;
            #print(article_time+" -  "+articleHolder)
            #print(article_url)
            try:
              article_content= GetWSJContent(article_url)
            except:           
              continue        
            
            lstarticle = [stock, article_FormattedDate, articleHolder, article_url, article_content]                   
            df2 = pd.DataFrame([lstarticle], columns=cols)        
            df_articles = df_articles.append(df2)
            AllArticles.append(lstarticle)  
    return df_articles, AllArticles
