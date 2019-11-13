# Removing Duplicates (Similarity scoring)
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

similarity_threshold = 0.5
vectorizer = TfidfVectorizer(min_df = 1, stop_words = 'english', use_idf=False, ngram_range=(1,2))

def RemoveDuplicates(stocks, df_articles):
    for stock in stocks:
        df1 = df_articles[df_articles.Ticker == stock]
        #dfname = "df_"+stock+"_articles"
        df_stock_articles = df1[df1['Text']!='']
        print('Articles With Content: ' +str(len(df_stock_articles)) + " for "+stock)
        print("-----------Removing Duplicates------------")
        articles = df_stock_articles['Text'].sort_index(ascending = False)
        if(len(articles)>0):
          dtm = vectorizer.fit_transform(articles)
          doc_term_matrix = pd.DataFrame(dtm.toarray(),index=articles,columns=vectorizer.get_feature_names())
          similarity = np.asarray(np.asmatrix(doc_term_matrix) * np.asmatrix(doc_term_matrix).T)
          similarity = np.triu(similarity, k=1)
          df_sim = pd.DataFrame(similarity, columns = articles)
          unique_articles = df_sim[(df_sim<=similarity_threshold)].dropna(axis = 1, how = 'any').columns.values
          df_articles['Unique_'+stock] = df_articles['Text'].apply(lambda x: 1 if x in unique_articles else 0)

        col_list = [col for col in df_articles.columns if 'Unique' in col]
        df_articles['Unique'] = df_articles[col_list].sum(axis=1)
        df_unique = df_articles[df_articles['Unique']>=1]
        print('Number Of Unique Articles: ' +str(len(df_unique)))
    return df_unique
    