from urllib.request import urlopen
import Common
from datetime import date, timedelta
from datetime import datetime
from dateutil import parser
import pandas as pd
import urllib
import bs4 as bs

def GetYahoofinContent(article_link):  
    strContent=''    
    url = article_link
    req = urllib.request.Request(url, headers={'User-Agent': 'IE9'})
    sourcehtml = urlopen(req)   
    soup = bs.BeautifulSoup(sourcehtml,"lxml")
    pbullets = soup.findAll("p")    
    for bullet in pbullets:
        bulletHolder = bullet.get_text().strip() 
        strContent = strContent + bulletHolder 
                
    return strContent 

#------------ Yahoo Fin Parser-------------

def GetArticles(stocks, last_date):
    cols=['Ticker','Date','Title','Link','Text']
    df_articles = pd.DataFrame([],columns=cols)   
    AllArticles = []
    for stock in stocks :
        url = "https://finance.yahoo.com/quote/"+stock+"/news?p="+stock
        req = urllib.request.Request(url, headers={'User-Agent' : "foobar"})
        sourcehtml = urlopen(req)
        soup = bs.BeautifulSoup(sourcehtml,"lxml")

        #Parse the document using soup object and extract the required text 
        mydivs = soup.findAll("h3", {"class":"Mb(5px)"}) 
        mydiv_time = soup.findAll("div", {"class":"C(#959595) Fz(11px) D(ib) Mb(6px)"})
        mydiv_url = soup.findAll("span", {"class":"headline"})   
        print("----------------------------------"+stock+"------------------------------------")
    
        for i,div in enumerate(mydivs):  
            atextHolder = div.findAll('a')
            articleHolder = atextHolder[0].get_text().strip()
            articlehref = atextHolder[0]['href']
            articleLink = articlehref
            artTime = mydiv_time[i].get_text().split('•')[1:2]
            strtime = ''.join(artTime)
            article_time =  datetime.now()
        
            #format article time
            today = datetime.now()
            if strtime.find("minute")!= -1:
                minute = int(strtime[:2])
                article_time = datetime.now() - timedelta(minutes=minute)
                acttime = (format(datetime.now() - timedelta(minutes=minute), "%m-%d-%Y %I:%M%p"))
                print (acttime)
            elif strtime.find("hour")!= -1:
                hour = int(strtime[:2])
                article_time = datetime.now() - timedelta(hours=hour)
                acttime = (format(datetime.now() - timedelta(hours=hour), "%m-%d-%Y %I:%M%p"))
                print (acttime)
            elif strtime.find("yesterday")!= -1:
                article_time = datetime.now() - timedelta(days=1)
                acttime =(format(datetime.now() - timedelta(days=1),"%m-%d-%Y %I:%M%p"))
                print (acttime)
            elif strtime.find("days")!= -1:
                dayz = int(strtime[:2])
                article_time = datetime.now() - timedelta(days=dayz)
                acttime =(format(datetime.now() - timedelta(days=dayz),"%m-%d-%Y %I:%M%p"))
                print (acttime)
            else:
                try:
                     acttime = (format(strtime, "%m-%d-%Y %I:%M%p"))
                     print (acttime)
                except:           
                     continue
           
           
            print (articleHolder)
       
            if  article_time.date() < last_date :
                break;
        
            #url = mydiv_url[i].find('a').attrs['href']
            if articlehref.find(".com") != -1:
                print(articlehref)
            else:
                articleLink = 'https://finance.yahoo.com'+articlehref
                print('https://finance.yahoo.com'+articlehref)
            print("\n")
            try:
              article_content= GetYahoofinContent(articleLink)
            except:           
              continue  
        
            #print(article_content)
            lstarticle = [stock, acttime, articleHolder, articleLink, article_content]
            df2 = pd.DataFrame([lstarticle], columns=cols)        
            df_articles = df_articles.append(df2)
            AllArticles.append(lstarticle)    
    return df_articles, AllArticles
