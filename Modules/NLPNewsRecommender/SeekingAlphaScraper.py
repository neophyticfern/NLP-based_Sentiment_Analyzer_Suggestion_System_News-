import bs4 as bs
import csv
import requests
import urllib
from urllib.request import urlopen

# Seeking Alpha News Parser

stocks = ["FB"]
AllArticles=[]
for stock in stocks :  
 url = "https://seekingalpha.com/symbol/"+stock+"?s="+stock
 #print(url)
    
 req = urllib.request.Request(url, headers={'User-Agent' : "foobar"})
 sourcehtml = urlopen(req)
 soup = bs.BeautifulSoup(sourcehtml,"lxml")

#Parse the document using soup object and extract the required text 
 analysisDiv = soup.find("div", {"class": "feed analysis"})
 NewsDiv = soup.find("div", {"class": "feed news"})
 myNewsContentdivs = NewsDiv.findAll("div", {"class": "content"})
 myAnalysisContentdivs = analysisDiv.findAll("div", {"class": "content"})
    
 Top5 = 0
 Top2 = 0
 print("-----------"+stock+"------------")
 for Contentdiv in myNewsContentdivs:
        
      if(Top5 >= 5):
        break;
        
      #Date Div
      Datediv = Contentdiv.find("div", {"class": "date_on_by"})
      DateText = Datediv.get_text()
      strs = DateText.split("•")
      SaveDate = "Today"
    
      #If I do not have Date information, not considering the article for now.
      if(len(strs)>=2):       
       SaveDate = strs[1]
       if SaveDate.find(",") == -1:            
          SaveDate = strs[2]       
      else:
        break;
        
      SaveDateFormatted  = ConvertDate(SaveDate)
     
      
      #Article Div        
      Articlediv = Contentdiv.find("div", {"class": "symbol_article"})
       #Extract Article
      atextHolder = Articlediv.findAll('a')
      articleHolder = atextHolder[0].get_text().strip()
      articlehref = atextHolder[0]['href']      
      print(SaveDate +" -  "+articleHolder) 
      articleLink = articlehref
      if articlehref.find(".com") != -1:            
          print(articlehref)
      else:
          articleLink = 'https://seekingalpha.com'+articlehref
          print('https://seekingalpha.com'+articlehref)
          article_content = GetSeekingAlphaContent(articleLink)
          print(article_content)
    
      print("\n")
      lstarticle = [stock, SaveDateFormatted, articleHolder, articleLink, article_content]
      AllArticles.append(lstarticle)
      Top5 = Top5 + 1
    
    
 for Contentdiv in myAnalysisContentdivs:
        
      if(Top2 >= 2):
        break;
        
      #Date Div
      Datediv = Contentdiv.find("div", {"class": "date_on_by"})
      DateText = Datediv.get_text()
      strs = DateText.split("•")
      SaveDate = "Today"
    
      #If I do not have Date information, not considering the article for now.
      if(len(strs)>=2):       
       SaveDate = strs[1]
       if SaveDate.find(",") == -1:            
          SaveDate = strs[2]       
      else:
        break;
      SaveDateFormatted  = ConvertDate(SaveDate)
      
      #Article Div        
      Articlediv = Contentdiv.find("div", {"class": "symbol_article"})
       #Extract Article
      atextHolder = Articlediv.findAll('a')
      articleHolder = atextHolder[0].get_text().strip()
      articlehref = atextHolder[0]['href']      
      print(SaveDate +" -  "+articleHolder) 
      articleLink = articlehref
      if articlehref.find(".com") != -1:            
          print(articlehref)
      else:
          articleLink = 'https://seekingalpha.com'+articlehref
          print('https://seekingalpha.com'+articlehref)
          article_content = GetSeekingAlphaContent(articleLink)
    
      print("\n")
      lstarticle = [stock, SaveDateFormatted, articleHolder, articleLink, article_content]
      AllArticles.append(lstarticle)
      Top2 = Top2 + 1
       
AllArticles
