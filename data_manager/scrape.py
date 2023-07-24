# automate fetching of holidays?
# eg. future good fridays, and other year dependent holidays that can't be hardcoded
# automate fetching of stock prices and updating the dataset

import yfinance as yf
import datetime
import pandas
from data_manager.manage import save_database


def get_stocks(dates, ticker):
    stocks = []
    for date in dates:
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        start = date_obj.strftime('%Y-%m-%d')
        end = (date_obj + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        stock = yf.download(ticker, start, end)
        entry = {
            "date": start,
            "close": stock['Close']
        }
        stocks.append(entry)
    return pandas.DataFrame(stocks).set_index('Date')


def build_database(till_date, ticker):
    try:
        db = yf.download(ticker, end=till_date).reset_index()
        db = db[['Date', 'Close']]
        save_database(db, ticker, till_date)
    except error as error:
        print(f'Error occured in fetching stocks: {error}')


# print(get_stocks(['2023-07-10', '2023-07-11', '2023-07-12'], "AAPL"))
