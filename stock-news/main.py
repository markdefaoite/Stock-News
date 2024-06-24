import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

TWILIO_SID = '## provided by Twilio ##'
TWILIO_AUTH_TOKEN = '## provided by Twilio ##'

AlphaVantage_api = "XBYW8H89B0WEAJSN"
news_api = "0a55c05c38d64083a119e3d7ca45879f"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": AlphaVantage_api
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference = (float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(yesterday_closing_price)) * 100)

if abs(diff_percent) > 5:
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": news_api,
    }

    response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = response.json()["articles"]

    three_articles = articles[:3]
    print(three_articles)

    formatted_articles = [
        f"{STOCK}: {up_down}{diff_percent}\nHeadline: {article['title']}. \nBrief: {article['description']}" for article
        in
        three_articles]
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="## Number provided by Twilio ##",
            to="## My Phone Number ##"
        )
