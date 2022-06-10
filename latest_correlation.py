"""
Scrape the website for texts and prices
"""

from bs4 import BeautifulSoup as bs
import requests
import re
import datetime
from datetime import datetime
import pandas as pd
import nltk
nltk.download('popular')
from nrclex import NRCLex
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np


api_key = "QUYCQ"


def find_between(s, first, last):
    try:
        regex = rf'{first}(.*?){last}'
        return re.findall(regex, s)
    except ValueError:
        return -1

def get_response_prices() -> requests.models.Response:
    headers = {
        "API-Key": api_key,
    }
    return requests.get('http://orderbookz.com/company', headers=headers)


def get_response_news() -> requests.models.Response:
    headers = {
        "API-Key": api_key,
    }
    return requests.get('http://orderbookz.com/news', headers=headers, verify=False)

def scrape_prices() -> None:
    """
    Scrape date, time and price.
    :return:
    """
    response = get_response_prices()
    soup = bs(response.text, "html")
    container = None
    try:
        container = soup.find_all("tr")[1:]
    except ValueError as e:

        print(e)


    # Get the time of the next update
    time = "9/6/2022 " + soup.find('p').getText().split(" ")[-1]
    print(time)
    time_untill_update = datetime.strptime(time, "%d/%m/%Y %H:%M:%S")
    current_time = datetime.now()
    print(f"time to update {time_untill_update} time now {current_time}")
    diff = time_untill_update - current_time
    print(diff)

    # # Get the prices
    l = []
    print("\n\n")
    for th in container:
        row = []
        for line in th:
            line = str(line)
            if len(line) == 0:
                continue
            data= find_between(line, "<td>", "</td>")
            try:
                row.append(data[0])
            except Exception as e:
                print(e)
        l.append(row)

    print(f"the list l {l}")
    print(len(l))
    prices_df = pd.DataFrame(l, columns = ["Date", "Time","Profit over Previous Period"])
    print(prices_df)
    
    return prices_df

    # add the dataframe


    # TODO: clean the data to the format that we want



def scrape_text() -> None:
    """
    Scrapes the news including company name and the text itself.
    :return:
    """
    response = get_response_news()
    soup = bs(response.text, "html")
    l = []
    try:
        container = soup.find_all("div", {"class": "card text-white bg-success"})

    except ValueError as e:
        print(e)

    # card - header
    try:
        container = soup.find_all("div", {"class": "card-header"})
        for i in container:
            company_name = i.get_text().strip()
            l.append([company_name])
            print(company_name)

    except ValueError as e:
        print(e)
   # card-body
    try:
        container = soup.find_all("div", {"class": "card-body"})
        print(type(container[0]))
        print(container)
        for i, text in enumerate(container):
            text = text.get_text().strip()
            l[i].append(text)

    except ValueError as e:
        print(e)

    try:
        container = soup.find_all("div", {"class": "card-footer text-muted"})
        print(container)
        for i, text in enumerate(container):
            text = text.get_text().strip()
            l[i].append(text)

    except ValueError as e:
        print(e)
    print(l)

    text_df = pd.DataFrame(l, columns=["Company", "News", "Time"])
    print(text_df)
    
    return text_df
    

    # TODO: clean data and put it in the correct format


if __name__ == "__main__":
    # print(":ff")
    prices_df = scrape_prices()
    news_df = scrape_text()





###### SENTIMENT ANALYSIS ######

######## NRCLEX / NLTK #########
nrc_scores = []

# Get a sentiment score for each comment
for item in news_df.News:
    NRCLex_object = NRCLex(item)
    NRCLex_score = NRCLex_object.affect_frequencies
    # because sometimes we get anticip and anticipation with values for anticip if there is no anticipation
    if len(NRCLex_score.keys()) > 10:
        del NRCLex_score['anticip']
    else:
        NRCLex_score['anticipation'] = NRCLex_score.pop('anticip')
    nrc_scores.append(list(NRCLex_score.values())) # I need to create a list, because we can't pickle dictionary items


# Create a dataframe of the scores
df_NRCLex_scores = pd.DataFrame(nrc_scores, columns = NRCLex_score.keys())

# Add the comment and time to the dataframe
df_NRCLex_scores.insert(0,'text', news_df.News)
df_NRCLex_scores.insert(1, 'time', news_df.Time)


####### VADER ########

# Initialize the Vader Sentiment
vader_analyzer = SentimentIntensityAnalyzer()

vader_scores = []

# Get a sentiment score for each comment
for item in news_df.News:
    vader_score = vader_analyzer.polarity_scores(item)
    vader_scores.append(list(vader_score.values())) # I need to create a list, because we can't pickle dictionary items

# Create a dataframe of the scores
df_vader_scores = pd.DataFrame(vader_scores, columns = vader_score.keys())

# Add the comment and time to the dataframe
df_vader_scores.insert(0,'text', news_df.News)
df_vader_scores.insert(1, 'time', news_df.Time)


######### TEXTBLOB ##########

# polarity is negative/positive
# subjectivity is objective = 0 and subjective = 1
news_polarity = []
news_subjectivity = []


for item in news_df.News:
    textblob_analyzer = TextBlob(item)
    polarity = textblob_analyzer.sentiment.polarity
    subjectivity = textblob_analyzer.sentiment.subjectivity
    news_polarity.append(polarity)
    news_subjectivity.append(subjectivity)

df_textblob_scores = pd.DataFrame()
df_textblob_scores['text'] = news_df.News
df_textblob_scores['time'] = news_df.Time
df_textblob_scores['polarity'] = news_polarity
df_textblob_scores['subjectivity'] = news_subjectivity


# To excel
df_NRCLex_scores.to_excel('NRClex_scores.xlsx')
df_textblob_scores.to_excel('Texblob_scores.xlsx')
df_vader_scores.to_excel('Vader_scores.xlsx')


prices_df["Time"] = pd.to_datetime(prices_df["Date"] + " " + prices_df["Time"])
del prices_df["Date"]

df_vader_scores["time"] = pd.to_datetime(df_vader_scores["time"])
df_NRCLex_scores["time"] = pd.to_datetime(df_NRCLex_scores["time"])
df_textblob_scores["time"] = pd.to_datetime(df_NRCLex_scores["time"])

prices_df.sort_values("Time", 0, ascending=True, inplace = True)
df_vader_scores.sort_values("time", 0, ascending=True, inplace = True)
df_NRCLex_scores.sort_values("time", 0, ascending=True, inplace = True)
df_textblob_scores.sort_values("time", 0, ascending=True, inplace = True)

start_index = 0
added_scores = []

for i in range(1,len(prices_df)):
    # mask = ((df_textblob_scores.loc[:,"time"] > prices_df.loc[:,"Time"].iloc[i-1]) & (df_textblob_scores.loc[:,"time"] <= prices_df.loc[:,"Time"].iloc[i]))
    # data = np.sum(df_textblob_scores.loc[mask])
    # added_scores.append(data["polarity"])
    
    mask = ((df_vader_scores.loc[:,"time"] > prices_df.loc[:,"Time"].iloc[i-1]) & (df_vader_scores.loc[:,"time"] <= prices_df.loc[:,"Time"].iloc[i]))
    data = np.sum(df_vader_scores.loc[mask])
    added_scores.append(data["compound"])

added_scores.append(0)
import matplotlib.pyplot as plt
plt.scatter(np.array(added_scores), prices_df.loc[:,"Profit over Previous Period"].astype(float))
    




            
        

