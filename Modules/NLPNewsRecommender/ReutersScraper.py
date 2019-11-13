from urllib.request import urlopen
import Common
from datetime import date, timedelta
from datetime import datetime
from dateutil import parser
import pandas as pd
import urllib
import bs4 as bs
import Common

def GetReutersContent(article_link):  
    strContent=''    
    url = article_link
    req = urllib.request.Request(url, headers={'User-Agent': 'IE9'})
    sourcehtml = urlopen(req)   
    soup = bs.BeautifulSoup(sourcehtml,"lxml")
    #print(soup)
    ReutersMaindiv = soup.find("div", {"class":"StandardArticleBody_body"})  
    #print(ReutersMaindiv)
    pbullets = ReutersMaindiv.findAll("p")    
    for bullet in pbullets:
        bulletHolder = bullet.get_text().strip() 
        strContent = strContent + bulletHolder     
    
    return strContent  

#------------ Reuters News Parser-------------

def GetArticles(stocks, last_date):
    cols=['Ticker','Date','Title','Link','Text']
    df_articles = pd.DataFrame([],columns=cols)   
    AllArticles = []
    for stock in stocks :   
        url = "https://www.reuters.com/finance/stocks/overview/"+stock 
        req = urllib.request.Request(url, headers={'User-Agent' : "foobar"})
        sourcehtml = urlopen(req)
        soup = bs.BeautifulSoup(sourcehtml,"lxml")
    
        #Parse the document using soup object and extract the required text 
        Newsdiv = soup.find("div", {"id":"companyOverviewNews"})   
        ModuleDiv = Newsdiv.find("div", {"class":"moduleBody"}) 
        FeatureDivs = ModuleDiv.findAll("div", {"class":"feature"}) 
        #print(len(FeatureDivs))
    
    
        mydiv_url = soup.findAll("span", {"class":"headline"})
    
        print("-----------"+stock+"------------")

        for i,div in enumerate(FeatureDivs): 
            atextHolder = div.findAll('a')       
            articleHolder = atextHolder[0].get_text().strip()        
            article_url =  "https://www.reuters.com/"+ atextHolder[0].attrs['href']   
            div_time = div.find("div", {"class":"relatedInfo"})
            span_time = div_time.find("span", {"class":"timestamp"}) 
            article_time = span_time.get_text().strip()
            article_FormattedDate = Common.ConvertDate(article_time)

            try:
                article_date = parser.parse(article_FormattedDate)
                print(article_date)
            except:           
                article_date = datetime.now()
                print('in except')

            if  article_date.date() < last_date :
                break;
            print(article_time+" -  "+articleHolder)
            print(article_url)
            article_content = GetReutersContent(article_url)
            
            lstarticle = [stock, article_FormattedDate, articleHolder, article_url, article_content]       
            df2 = pd.DataFrame([lstarticle], columns=cols)        
            df_articles = df_articles.append(df2)
            AllArticles.append(lstarticle)
    return df_articles, AllArticles
