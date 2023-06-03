import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc."

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "SGF73W8D0NPIJINV"
NEWS_API_KEY = "c3db245c5cb442f6ac757fafb8a07e88"
account_sid = 'AC319ee8e3e551fb82cd012ad8ce97fef4'
auth_token = 'AUTHORIZATION TOKEN'
icon: str


# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params = {
    'function': "TIME_SERIES_DAILY_ADJUSTED",
    'symbol': STOCK_NAME,
    'apikey': STOCK_API_KEY
}
# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries.
#  e.g. [new_value for (key, value) in dictionary.items()]
response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
yesterday = response.json()['Time Series (Daily)']
yesterday_data = list(yesterday.values())[0]
yesterday_closing_price = yesterday_data['4. close']

# TODO 2. - Get the day before yesterday's closing stock price
last_yesterday_data = list(yesterday.values())[1]
last_yesterday_closing = last_yesterday_data['4. close']

# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
#  Hint: https://www.w3schools.com/python/ref_func_abs.asp
absolute_difference = abs(float(yesterday_closing_price) - float(last_yesterday_closing))
difference = float(yesterday_closing_price) - float(last_yesterday_closing)
if difference > 0:
    icon = '🔺'
elif difference < 0:
    icon = '🔻'

# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day
#  before yesterday.
percentage_difference = round((absolute_difference / float(yesterday_closing_price)) * 100, 2)

# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if percentage_difference >= 5:
    fluctuation = True
else:
    fluctuation = False

# STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
news_params = {
    'q': COMPANY_NAME,
    'from': list(yesterday.keys())[0],
    'to': list(yesterday.keys())[1],
    'sortBy': "popularity",
    'apikey': NEWS_API_KEY
}
# TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
news = requests.get(url=NEWS_ENDPOINT, params=news_params)
articles = news.json()['articles']

# TODO 7. - Use Python slice operator to create a list that contains the first 3 articles.
#  Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
news = articles[:3]

# STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
news_titles = [article['title'] for article in news]
news_description = [article['description'] for article in news]

# TODO 9. - Send each article as a separate message via Twilio.
if fluctuation:
    client1 = Client(account_sid, auth_token)
    message1 = client1.messages.create(
        body=f'''{COMPANY_NAME}: {icon}{percentage_difference}%
             Headline: {news_titles[0]}. 
             Brief: {news_description[0]}''',
        from_='+13612739661',
        to='PHONE NUMBER'
    )
    client2 = Client(account_sid, auth_token)
    message2 = client2.messages.create(
        body=f'''{COMPANY_NAME}: {icon}{percentage_difference}%
                 Headline: {news_titles[1]}. 
                 Brief: {news_description[1]}''',
        from_='+13612739661',
        to='PHONE NUMBER'
    )
    client3 = Client(account_sid, auth_token)
    message3 = client3.messages.create(
        body=f'''{COMPANY_NAME}: {icon}{percentage_difference}%
                 Headline: {news_titles[2]}. 
                 Brief: {news_description[2]}''',
        from_='+13612739661',
        to='PHONE NUMBER'
    )
