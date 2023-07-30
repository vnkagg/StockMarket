# automate fetching of holidays?
# eg. future good fridays, and other year dependent holidays that can't be hardcoded
# automate fetching of stock prices and updating the dataset

import yfinance as yf
import datetime
import pandas as pd
from data_manager.manage import save_database
from data_manager.features import clean_features

# during prediction
n_features = 2

# def find_last_existing_stock(date, ticker):
#     date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
#     end = date_obj.strftime('%Y-%m-%d')
#     start = (date_obj - datetime.timedelta(days=n_features)).strftime('%Y-%m-%d')
#     try:
#         fetched = yf.download(ticker, start=start, end=end)
#         return end, fetched['Close'].values
#     except:
#         previous_day = (date_obj - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
#         return find_last_existing_stock(previous_day, ticker)


# def get_stocks(dates, ticker):
#     df = pd.DataFrame()
#     for date in dates:
#         date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
#         end = date_obj.strftime('%Y-%m-%d')
#         start = (date_obj - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
#         last_existing_date = find_last_existing_stock(date, ticker)
#         prepare(last_existing_date, date, ticker)
#         # predict for last_existing_date -> date so that you can predict for date

#         # stock = yf.download(ticker, start=start,
#         #                     end=end)['Close'].reset_index()
#         # temp_df = clean_features(stock)
#         # print(temp_df)
#         # df = pd.concat([df, temp_df])
#         # df = pd.concat([df, temp_df.loc[date]])
#     return df


# during training/ refreshing everyday
def build_database(start_date, till_date, ticker):
    try:
        db = yf.download(ticker, start=start_date,
                         end=till_date).reset_index()
        db = db[['Date', 'Close']]
        save_database(db, ticker, till_date)
    except error as error:
        print(f'Error occured in fetching stocks: {error}')


# print(get_stocks(['2023-07-10', '2023-07-11', '2023-07-12'], "AAPL"))
