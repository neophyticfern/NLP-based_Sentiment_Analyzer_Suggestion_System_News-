import pandas as pd
from datetime import date, timedelta
from datetime import datetime
import StockMovement

def CreateDashboard(stocks, df_unique):
    final_output_str = ''
    pd.set_option('display.max_colwidth', 200)
    for stock in stocks:
        positive = str(len(df_unique[(df_unique['Sentiment'] == 'Positive') & (df_unique['Ticker'] == stock)]))
        negative = str(len(df_unique[(df_unique['Sentiment'] == 'Negative') & (df_unique['Ticker'] == stock)]))
        neutral = str(len(df_unique[(df_unique['Sentiment'] == 'Neutral') & (df_unique['Ticker'] == stock)]))
        df_stock = df_unique[df_unique['Ticker'] == stock]
        df_stock['abs_sentiment'] = df_stock['Score'].abs()
        df_stock =df_stock.sort_values(by= 'abs_sentiment', ascending=False).head(5)
        df_final= df_stock.drop('abs_sentiment', axis=1)

        df_final = StockMovement.AddMovementToDF(df_final)

        print("-----------Creating html file------------")
        print("for" + stock)
        #write html file
        html_file_nm = 'ImportantArticles'+ datetime.now().strftime('%Y-%m-%d-%H-%M') +'.html'
        df_final.to_html(html_file_nm)
        ### to_html(feed name of file)

        ###### CREATE HTML CONTENT ###########
        with open(html_file_nm, 'r') as f:
            html_content_full = f.readlines()
            ####readlines: reads the entire file and converts it to a list
        print(html_content_full)

        new_html_content_full = []

        for elem in html_content_full:
          ##find to search
          if elem.find('table') > 0:
            ##if it finds table it will manipulate elem to add css
            re = '<table border="1" style="color:black;background-color:lavender" class="dataframe">\n'
            new_html_content_full.append(re)
          elif elem.find('http:') > 0:
            index_start = elem.index('>')
            end_index = elem.index('</td>')
            ##one quote for href and one for python string
            re = '<td>' + '<a  href="' + elem[index_start+1:end_index] + '">' +  elem[index_start+1:end_index] + '</a>'
            new_html_content_full.append(re)
          elif elem.find('https:') > 0:
            index_start = elem.index('>')
            end_index = elem.index('</td>')
            ##one quote for href and one for python string
            re = '<td>' + '<a  href="' + elem[index_start+1:end_index] + '">' +  elem[index_start+1:end_index] + '</a>'
            new_html_content_full.append(re)
          else:
            new_html_content_full.append(elem)

        html_content = ''
        html_content += '<body style="background-image: url(Framebg.jpg)">'+'</body><br>'
        html_content += '<h1 style="background-color:lightsteelblue; opacity:0.7;text-align:center, border:double">' + stock + '</h1></br>'
        html_content += \
        '<div style="background-color:lavender; border:double;float: left; width:10%; text-align:center;height:4%; padding-top:0.5%">Positive:' + positive + '</div><div style="float: left;"> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</div>' \
        '<div style="background-color:lavender; border:double;float: left; width:10%; text-align:center;height:4%; padding-top:0.5%"">  Negative:' + negative + '</div><div style="float: left;"> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</div>' \
        '<div style="background-color:lavender; border:double;float: left; width:15%; text-align:center;height:4%; padding-top:0.5%""> Neutral:' + neutral + '</div><br/><br/><br/><br/>'

        new_html_content_full.insert(0,html_content)
        final_output_str += ''.join(new_html_content_full)
        final_output_str += '<br/><br/><br/><br/>'

    with open('ImportantArticles'+ datetime.now().strftime('%Y-%m-%d-%H-%M') +'.html', 'w+') as f:
            f.write(final_output_str)

def CreateDashboardWithTweets(stocks, df_unique, tweet_df):
    final_output_str = ''
    pd.set_option('display.max_colwidth', 200)
    for stock in stocks:
        positive = str(len(df_unique[(df_unique['Sentiment'] == 'Positive') & (df_unique['Ticker'] == stock)]))
        negative = str(len(df_unique[(df_unique['Sentiment'] == 'Negative') & (df_unique['Ticker'] == stock)]))
        neutral = str(len(df_unique[(df_unique['Sentiment'] == 'Neutral') & (df_unique['Ticker'] == stock)]))
        pos_tweets = str(len(tweet_df[(tweet_df['Ticker'] == stock) & (tweet_df['Sentiment'] == 'Positive')]))
        print('pos_tweets :')
        print(pos_tweets)
        neg_tweets = str(len(tweet_df[(tweet_df['Ticker'] == stock) & (tweet_df['Sentiment'] == 'Negative')]))
        neutral_tweets = str(len(tweet_df[(tweet_df['Ticker'] == stock) & (tweet_df['Sentiment'] == 'Neutral')]))
        df_stock = df_unique[df_unique['Ticker'] == stock]
        df_stock['abs_sentiment'] = df_stock['Score'].abs()
        df_stock =df_stock.sort_values(by= 'abs_sentiment', ascending=False).head(5)
        df_final= df_stock.drop('abs_sentiment', axis=1)
        df_final = StockMovement.AddMovementToDF(df_final)
        df_final['Close'] = df_final['Close'].apply(lambda x: round(x,2))
        if len(df_final.index) > 0:
          print("-----------Creating html file------------")
          print("for" + stock)
          #write html file
          html_file_nm = 'ImportantArticles'+ datetime.now().strftime('%Y-%m-%d-%H-%M') +'.html'
          cols = [c for c in df_final.columns if c.lower()[:6] != 'unique']        
          df_final_noUnique=df_final[cols]          
          df_final_noUnique.to_html(html_file_nm)
          ### to_html(feed name of file)

          ###### CREATE HTML CONTENT ###########
          with open(html_file_nm, 'r') as f:
              html_content_full = f.readlines()
              ####readlines: reads the entire file and converts it to a list
          print(html_content_full)

          new_html_content_full = []

          for elem in html_content_full:
            ##find to search
            if elem.find('table') > 0:
              ##if it finds table it will manipulate elem to add css
              re = '<table border="1" style="color:black;background-color:lavender" class="dataframe">\n'
              new_html_content_full.append(re)
            elif elem.find('http:') > 0:
              index_start = elem.index('>')
              end_index = elem.index('</td>')
              ##one quote for href and one for python string
              re = '<td>' + '<a  href="' + elem[index_start+1:end_index] + '">' +  elem[index_start+1:end_index] + '</a>'
              new_html_content_full.append(re)
            elif elem.find('https:') > 0:
              index_start = elem.index('>')
              end_index = elem.index('</td>')
              ##one quote for href and one for python string
              re = '<td>' + '<a  href="' + elem[index_start+1:end_index] + '">' +  elem[index_start+1:end_index] + '</a>'
              new_html_content_full.append(re)
            else:
              new_html_content_full.append(elem)
          html_content = ''
          html_content += '<body style="background-image: url(1.jpg)">'+'</body><br>'
          html_content += '<h1 style="background-color:lightsteelblue; border:solid lavender; opacity:0.7;text-align:center, border:double">' + stock + '</h1></br>'
          html_content += \
          '<div style="background-color:lavender; border:double;float: left; width:15%; text-align:center;height:4%; padding-top:0.5%">Positive : '+ positive +'</div>'\
          '<div style="background-color:white;float: left; width:25%; text-align:center;height:4%; padding-top:0.5%"></div>'\
          '<div></div>'\
          '<div style="background-color:lavender; border:double;float: left; width:15%; text-align:center;height:4%; padding-top:0.5%">negative : ' + negative + '</div>'\
          '<div style="background-color:white; float: left; width:25%; text-align:center;height:4%; padding-top:0.5%"></div>'\
          '<div></div>'\
          '<div style="background-color:lavender; border:double;float: left; width:15%; text-align:center;height:4%; padding-top:0.5%">Neutral : ' + neutral + '</div><br/>'\
          '<br/>'\
          '<br/>'\
          '<br/>'\
          '<div style="background-color:lavender; border:double;float: left; width:15%; text-align:center;height:4%; padding-top:0.5%">Pos_Stocktwits : ' + pos_tweets + '</div>'\
          '<div style="background-color:white;float: left; width:25%; text-align:center;height:4%; padding-top:0.5%"></div>'\
          '<div></div>'\
          '<div style="background-color:lavender; border:double;float: left; width:15%; text-align:center;height:4%; padding-top:0.5%">Neg_Stocktwits : ' + neg_tweets + '</div>'\
          '<div style="background-color:white; float: left; width:25%; text-align:center;height:4%; padding-top:0.5%"></div>'\
          '<div></div>'\
          '<div style="background-color:lavender; border:double;float: left; width:15%; text-align:center;height:4%; padding-top:0.5%">Neu_Stocktwits : ' + neutral_tweets + '</div>'\
          '<br/>'\
          '<br/>'\
          '<br/>'
          new_html_content_full.insert(0,html_content)

          #html_content = ''
          #html_content += '<body style="background-image: url(1.jpg)">'+'</body><br>'
          #html_content += '<h1 style="background-color:lightsteelblue; border:solid lavender; opacity:0.7;text-align:center, border:double">' + stock + '</h1></br>'
          #html_content += \
          #'<div><div style="background-color:lavender; border:double;float: left; width:10%; text-align:center;height:4%; padding-top:0.5%">Positive:' + positive + '</div><div style="float: left;"> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</div>' \
          #'<div style="background-color:lavender; border:double;float: left; width:10%; text-align:center;height:4%; padding-top:0.5%">  Negative:' + negative + '</div><div style="float: left;"> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</div>' \
          #'<div style="background-color:lavender; border:double;float: left; width:15%; text-align:center;height:4%; padding-top:0.5%"> Neutral:' + neutral + '</div></div><br/>' \
          #'<div><div style="background-color:lavender; border:double;float: left; width:10%; text-align:center;height:4%; padding-top:0.5%">Pos_Stocktwits:' + pos_tweets + '</div><div style="float: left;"> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</div>' \
          #'<div style="background-color:lavender; border:double;float: left; width:10%; text-align:center;height:4%; padding-top:0.5%">Neg_stocktwits:' + neg_tweets + '</div><div style="float: left;"> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</div>' \
          #'<div style="background-color:lavender; border:double;float: left; width:15%; text-align:center;height:4%; padding-top:0.5%">Neu_Stocktwits:' + neutral_tweets + '</div></div><br/><br/><br/><br/><br/><br/>'
          #new_html_content_full.insert(0,html_content)
          final_output_str += ''.join(new_html_content_full)
          final_output_str += '<br/><br/><br/><br/>'

    with open('ImportantArticles'+ datetime.now().strftime('%Y-%m-%d-%H-%M') +'.html', 'w+') as f:
            f.write(final_output_str)
    print('Completed')
