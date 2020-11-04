import yfinance as yf
import streamlit as st
import datetime
import talib
import ta
import pandas as pd
import requests
yf.pdr_override()

st.write("""
# Stock Analysis Application
Shown below are the **Adjusted Close price**, **Moving Averages**, **Relative Strength Indexes**, **On Balance Volume** of any stock!
""")
#st.sidebar.header('Author: Prachi Yewale')
st.text("")
st.sidebar.header('Project: Stock Market Analysis and Prediction')
st.sidebar.header('Link to code:'
                  'https://github.com/prachicodes/Stock-Market-Prediction-and-Analysis-')

st.sidebar.header('Input the following parameters!')
#st.sidebar.header('Author: Prachi Yewale')

today = datetime.date.today()
def user_input_features():
    ticker = st.sidebar.text_input("Stock Name", 'AAPL')
    start_date = st.sidebar.text_input("Start Date", '2019-01-01')
    end_date = st.sidebar.text_input("End Date", f'{today}')
    return ticker, start_date, end_date

symbol, start, end = user_input_features()

def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
    result = requests.get(url).json()
    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']
company_name = get_symbol(symbol.upper())

start = pd.to_datetime(start)
end = pd.to_datetime(end)

# Read data
data = yf.download(symbol,start,end)

# Adjusted Close Price

#st.text_input("Close Price: Raw price which is just the cash value of the last transacted price before the market closes")
#st.header('Adjusted cloding price: It is teh close price that takes into account the factors like corporate actions, such as stock splits, dividends, and rights offerings')
st.header(f"Adjusted Close Price\n {company_name}")
st.line_chart(data['Adj Close'])

# ## SMA and EMA
#Simple Moving Average
st.text("")
data['SMA'] = talib.SMA(data['Adj Close'], timeperiod = 20)

# Exponential Moving Average
data['EMA'] = talib.EMA(data['Adj Close'], timeperiod = 20)

# Plot
st.header(f"Simple Moving Average vs. Exponential Moving Average\n {company_name}")
st.line_chart(data[['Adj Close','SMA','EMA']])

# ## RSI (Relative Strength Index)
# RSI
data['RSI'] = talib.RSI(data['Adj Close'], timeperiod=14)

# Plot
st.header(f"Relative Strength Index\n {company_name}")
st.line_chart(data['RSI'])

# ## OBV (On Balance Volume)
# OBV
data['OBV'] = talib.OBV(data['Adj Close'], data['Volume'])/10**6
# Plot
st.header(f"On Balance Volume\n {company_name}")
st.line_chart(data['OBV'])
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")


st.text('Author: Prachi Yewale')