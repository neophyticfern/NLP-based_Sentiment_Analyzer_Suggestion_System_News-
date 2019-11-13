import pandas_datareader.data as web
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import fix_yahoo_finance as yf
import datetime
pd.core.common.is_list_like = pd.api.types.is_list_like
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
import configparser
import ast

config = configparser.RawConfigParser()
config.read('Configuration.cfg')

# end day is today
today = datetime.datetime.today()
today.strftime('%m/%d/%Y')

# start day is 5 business days ago
US_BUSINESS_DAY = CustomBusinessDay(calendar=USFederalHolidayCalendar())
lastBusDay = today - 6 * US_BUSINESS_DAY
lastBusDay.strftime('%m/%d/%Y')

SP = web.DataReader('^GSPC', 'yahoo', lastBusDay, today)
SP = SP.iloc[::-1]
# generate dollar value of movement between adjacent business days
SP['Mov $'] = round(-SP['Close'].diff().shift(-1), 2)
# generate percentage of movement between adjacent business days
SP['Mov %'] = SP['Mov $']/SP['Close'].shift(-1)
SP = SP[:5].reset_index()

ticker_list = ast.literal_eval(config["DEFAULT"]["ticker_list"]) # if this doesn't work, then hard-code the tickers in, as given below
#ticker_list = ["ADBE", "BABA", "GOOG", "AMZN", "BIDU", "BKNG", "BZUN", "ENV", "FB", "GDDY", "MA", "NFLX", "MTCH", "MOMO", "PCTY", "PYPL", "RP", "CRM", "SINA", "SQ", "ZG", "CTRP", "MSFT", "NVDA", "WB", "WUBA"]
df_final = pd.DataFrame()

for ticker in ticker_list:
    df = web.DataReader(ticker, 'yahoo', lastBusDay, today)
    df['Ticker'] = ticker
    df = df.iloc[::-1]
    # generate dollar value of movement between adjacent business days
    df['Mov $'] = round(-df['Close'].diff().shift(-1), 2)
    # generate percentage of movement between adjacent business days
    df['Mov %'] = df['Mov $']/df['Close'].shift(-1)
    df_final = df_final.append(df[:5])

#df_final
df_final.reset_index(inplace=True)
#df_final

SP_final = SP[['Date','Mov %']]
#SP_final
df_final = df_final.merge(SP_final, on='Date', how='left').rename(index=str, columns={"Mov %_x": "Mov %_ST", "Mov %_y": "Mov %_SP"})
#df_final
df_final['Mov %']=df_final['Mov %_ST']-df_final['Mov %_SP']
df_final['Mov %'] = pd.Series(["{0:.2f}%".format(X * 100) for X in df_final['Mov %']], index = df_final.index)
df_final['Mov %_ST'] = pd.Series(["{0:.2f}%".format(X * 100) for X in df_final['Mov %_ST']], index = df_final.index)
df_final['Mov %_SP'] = pd.Series(["{0:.2f}%".format(X * 100) for X in df_final['Mov %_SP']], index = df_final.index)


def AddMovementToDF(articles):    
  articles['DateForm'] = pd.to_datetime(articles['Date']).dt.normalize()
  article_w_price_change = (articles.merge(df_final, how='left', left_on=['Ticker','DateForm'], right_on=['Ticker','Date'])).drop(['DateForm','High','Low','Open','Adj Close','Volume','Mov %','Date_y','Mov $'], axis=1)
  article_w_price_change.rename(columns={'Date_x':'Date'}, inplace=True)
  return article_w_price_change
