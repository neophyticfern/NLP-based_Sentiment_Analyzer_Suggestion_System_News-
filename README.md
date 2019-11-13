# NLP_news-recommendation
NLP-based system to recommend news articles according to sentiment and duplicity

This is a tool created to analyze news articles about any firm from the web and correlate with the firm's stock price. After pulling articles from the web, the program removes duplicates and other closely-related articles and scores the remaining articles for sentiment. These are then matched with the corresponding company's stock price movement and that in the S&P 500 index. It also provides an estimate of the investor sentiment by analyzing the polarity of the tweets from investors on the StockTwits platform.

In order to use this tool, the user will need to have Python 3 with all the requisite packages installed on the system. Following is a list of detailed instructions for installing the required packages and setting the configuration for each run. The authentication credentials required to use the StockTwits module will have to one's own - the one posted here is a placeholder.


## Step 1. Installing Python 3
There are several ways to install python 3. <https://www.python.org/> has all the versions.
For a guide on installing python please visit <https://realpython.com/installing-python/#windows>
    
## Step 2: Install Packages

**- SciPy**

$ python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose

<https://www.scipy.org/install.html>

If you are using pip version under 18, you might consider upgrading via the 'pip install --upgrade pip' command.
    
**- Sci-kit Learn**

$ pip install -U scikit-learn

<http://scikit-learn.org/stable/install.html>

**- Fix-Yahoo-Finance**

$ pip install fix_yahoo_finance

https://pypi.org/project/fix-yahoo-finance/


**- Pandas-Datareader**

$ pip install pandas-datareader might install version 0.6.0 which using the expired API, instead

install latest development version

$ pip install git+https://github.com/pydata/pandas-datareader.git

**- PySentiment**
$pip install pysentiment

https://pypi.org/project/pysentiment/

**-PyTwits**

- PySentiment $pip install pytwits

https://pypi.org/project/pytwits/
