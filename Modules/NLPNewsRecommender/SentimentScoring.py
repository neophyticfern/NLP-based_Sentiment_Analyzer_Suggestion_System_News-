import pysentiment as ps
 
def Sentiment(a):   
    try:
        lm = ps.LM()
        tokens = lm.tokenize(a)
        a= lm.get_score(tokens)['Polarity']
        if a>0:
            return "Positive" 
        elif(a==0):
            return "Neutral" 
        else:
            return "Negative" 
    except UnicodeDecodeError:
        return "Neutral"
    
def Score(a):  
    #try: 
        lm = ps.LM()
        tokens = lm.tokenize(a)
        polScore = lm.get_score(tokens)['Polarity']
        return polScore
    #except UnicodeDecodeError:
        #print('in UnicodeDecodeError')
        #return 0

def SentimentForScore(score):
    if score>0:
            return "Positive" 
    elif(score==0):
            return "Neutral" 
    else:
            return "Negative"

def ScoreArticles(df_unique):
  print("-----------Sentiment Scoring------------")
  df_unique['Score']=df_unique['Text'].apply(lambda x: Score(x))
  df_unique['Sentiment']=df_unique['Score'].apply(lambda x: SentimentForScore(x))
  return df_unique
