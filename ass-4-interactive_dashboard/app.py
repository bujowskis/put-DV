import streamlit as st
import pandas as pd
import pandas_datareader as web
import numpy as np
import seaborn as sns
import yfinance
from datetime import date, timedelta
import plotly.express as px
import plotly.io as pio


@st.cache
def get_data_today(tickers):
    data = pd.DataFrame()
    for tic in tickers:
        try:
            dt = web.DataReader(tic, "yahoo", date.today()-timedelta(days=250), date.today())["Adj Close"].dropna()           
            dt = dt.rename(tic)
            data = data.join(dt, how="outer")
        except KeyError:
            print("The market is closed today")
    data = data.fillna(method='ffill')
    return data


def price_ret_summary(tickers):
    data = get_data_today(tickers)
    p = pd.DataFrame()
    r = pd.DataFrame()
    for t in tickers:
        p.loc[t, "1d"] = data[t][-1]
        p.loc[t, "10d"] = data[t][-8]
        p.loc[t, "1m"] = data[t][-22]
        p.loc[t, "2m"] = data[t][-44]
        p.loc[t, "6m"] = data[t][-132]
        r.loc[t, "1d"] = ((data[t].pct_change())[-1])*100
        r.loc[t, "10d"] = ((data[t].pct_change(8))[-1])*100
        r.loc[t, "1m"] = ((data[t].pct_change(22))[-1])*100
        r.loc[t, "2m"] = ((data[t].pct_change(44))[-1])*100
        r.loc[t, "6m"] = ((data[t].pct_change(132))[-1])*100
    return p, r


select_page = st.sidebar.selectbox("Select a page:", options=("Dashboard", "Charts"))

# Dashboard
if select_page == "Dashboard":
    header = st.container()
    box1 = st.container()
    box2 = st.container()
    # Equity market indexes
    tickers1 = ["^GSPC", "^IXIC", "000001.SS", "^STOXX50E", "EEM", "^VIX"]
    price1, retsumm1 = price_ret_summary(tickers1) 
    price1.rename(index={"^GSPC":"S&P 500", "^IXIC":"NASDAQ", "000001.SS":"SSE Comp.", "^STOXX50E":"Eurostoxx50", "EEM":"Emerging Mkts", "^VIX":"VIX"}, inplace=True)
    retsumm1.rename(index={"^GSPC":"S&P 500", "^IXIC":"NASDAQ", "000001.SS":"SSE Comp.", "^STOXX50E":"Eurostoxx50", "EEM":"Emerging Mkts", "^VIX":"VIX"}, inplace=True)
    # Currencies
    tickers2 = ["EURUSD=X", "GBPUSD=X", "USDCNY=X", "GBPEUR=X", "BTC-USD", "ETH-USD"] 
    price2, retsumm2 = price_ret_summary(tickers2) 
    price2.rename(index={"EURUSD=X":"EUR/USD", "GBPUSD=X":"GBP/USD", "USDCNY=X":"Renminbi/USD", "GBPEUR=X":"GBP/EUR", "BTC-USD":"BTC/USD", "ETH-USD":"ETH/USD"}, inplace=True)
    retsumm2.rename(index={"EURUSD=X":"EUR/USD", "GBPUSD=X":"GBP/USD", "USDCNY=X":"Renminbi/USD", "GBPEUR=X":"GBP/EUR", "BTC-USD":"BTC/USD", "ETH-USD":"ETH/USD"}, inplace=True)
    # Commodities (futures)
    tickers3 = ["^BCOM", "GC=F", "CL=F", "SI=F", "PA=F", "ZW=F"]
    price3, retsumm3 = price_ret_summary(tickers3) 
    price3.rename(index={"^BCOM":"Comm.Index", "GC=F":"Gold", "CL=F":"Crude", "SI=F":"Silver", "PA=F":"Palladium", "ZW=F":"Wheat"}, inplace=True)
    retsumm3.rename(index={"^BCOM":"Comm.Index", "GC=F":"Gold", "CL=F":"Crude", "SI=F":"Silver", "PA=F":"Palladium", "ZW=F":"Wheat"}, inplace=True)
    
    with header:
        st.title("Financial Dashboard")
        st.write("Daily and monthly returns for indexes; Value and monthly return for currencies and commodities")
    
    with box1:
        # Equity market indexes
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("S&P 500", f"{retsumm1.loc['S&P 500', '1d']:.2f}%", f"{retsumm1.loc['S&P 500', '1m']:.2f}%", delta_color="off")
        col2.metric("NASDAQ", f"{retsumm1.loc['NASDAQ', '1d']:.2f}%", f"{retsumm1.loc['NASDAQ', '1m']:.2f}%", delta_color="off")
        col3.metric("SSE Comp.", f"{retsumm1.loc['SSE Comp.', '1d']:.2f}%", f"{retsumm1.loc['SSE Comp.', '1m']:.2f}%", delta_color="off")
        col4.metric("Eurostoxx50", f"{retsumm1.loc['Eurostoxx50', '1d']:.2f}%", f"{retsumm1.loc['Eurostoxx50', '1m']:.2f}%", delta_color="off")
        col5.metric("Emerging Mkts", f"{retsumm1.loc['Emerging Mkts', '1d']:.2f}%", f"{retsumm1.loc['Emerging Mkts', '1m']:.2f}%", delta_color="off")
        col6.metric("VIX", f"{price1.loc['VIX', '1d']:.2f}", f"{retsumm1.loc['VIX', '1d']:.2f}%")
        # Currencies
        col1.metric("EUR/USD", f"{price2.loc['EUR/USD', '1d']:.2f}", f"{retsumm2.loc['EUR/USD', '1m']:.2f}%")
        col2.metric("GBP/USD", f"{price2.loc['GBP/USD', '1d']:.2f}", f"{retsumm2.loc['GBP/USD', '1m']:.2f}%")
        col3.metric("Renminbi/USD", f"{price2.loc['Renminbi/USD', '1d']:.2f}", f"{retsumm2.loc['Renminbi/USD', '1m']:.2f}%")
        col4.metric("GBP/EUR", f"{price2.loc['GBP/EUR', '1d']:.2f}", f"{retsumm2.loc['GBP/EUR', '1m']:.2f}%")
        col5.metric("BTC/USD", f"{price2.loc['BTC/USD', '1d']:.2f}", f"{retsumm2.loc['BTC/USD', '1m']:.2f}%")
        col6.metric("ETH/USD", f"{price2.loc['ETH/USD', '1d']:.2f}", f"{retsumm2.loc['ETH/USD', '1m']:.2f}%")
        # Commodities
        col1.metric("Comm.Index", f"{retsumm3.loc['Comm.Index', '1d']:.2f}%", f"{retsumm3.loc['Comm.Index', '1m']:.2f}%", delta_color="off")
        col2.metric("Gold", f"{price3.loc['Gold', '1d']:.2f}", f"{retsumm3.loc['Gold', '1m']:.2f}%")
        col3.metric("Crude", f"{price3.loc['Crude', '1d']:.2f}", f"{retsumm3.loc['Crude', '1m']:.2f}%")
        col4.metric("Silver", f"{price3.loc['Silver', '1d']:.2f}", f"{retsumm3.loc['Silver', '1m']:.2f}%")
        col5.metric("Palladium", f"{price3.loc['Palladium', '1d']:.2f}", f"{retsumm3.loc['Palladium', '1m']:.2f}%")
        col6.metric("Wheat", f"{price3.loc['Wheat', '1d']:.2f}", f"{retsumm3.loc['Wheat', '1m']:.2f}%")

    with box2:
        st.subheader("Equity market indexes")
        st.dataframe(price1)
        st.dataframe(retsumm1.style.background_gradient(axis=1))
        st.subheader("Currencies")
        st.dataframe(price2)
        st.dataframe(retsumm2.style.background_gradient(axis=1))
        st.subheader("Commodities")
        st.dataframe(price3)
        st.dataframe(retsumm3.style.background_gradient(axis=1))

    st.sidebar.title("About")
    st.sidebar.info('This app is a simple interactive financial dashboard, created for Data Visualization course of Artificial Intelligence degree at the Poznań University of Technology.')


# Charts
if select_page == "Charts":
    header = st.container()
    box1 = st.container()

    with header:
        st.title("Charts")
    #@st.cache(ignore_hash=True)

    def load_quotes(asset):
        return yfinance.download(asset)

    def load_data():
        components = pd.read_html('https://en.wikipedia.org/wiki/List_of_S'
                    '%26P_500_companies')[0]
        return components.drop('SEC filings', axis=1).set_index('Symbol')

    def label(symbol):
        a = components.loc[symbol]
        return symbol + ' - ' + a.Security
    components = load_data()
    title = st.empty()
    if st.sidebar.checkbox('View companies list'):
        st.dataframe(components[['Security',
                                 'GICS Sector',
                                 'Date first added',
                                 'Founded']])

    st.sidebar.subheader('Select asset')
    asset = st.sidebar.selectbox('Click below to select a new asset',
                                 components.index.sort_values(), index=3,
                                 format_func=label)
    selected_stock=asset
    
    stock_data = yfinance.Ticker(selected_stock)
    title.title(components.loc[asset].Security)
    data0 = load_quotes(asset)
    data = data0.copy().dropna()
    data.index.name = None

    section = st.sidebar.slider('Number of quotes', min_value=30,
                        max_value=min([2000, data.shape[0]]),
                        value=500,  step=10)

    data2 = data[-section:]['Adj Close'].to_frame('Adj Close')

    sma = st.sidebar.checkbox('SMA')
    if sma:
        period= st.sidebar.slider('SMA period', min_value=5, max_value=500,
                             value=20,  step=1)
        data[f'SMA {period}'] = data['Adj Close'].rolling(period ).mean()
        data2[f'SMA {period}'] = data[f'SMA {period}'].reindex(data2.index)

    sma2 = st.sidebar.checkbox('SMA2')
    if sma2:
        period2= st.sidebar.slider('SMA2 period', min_value=5, max_value=500,
                             value=100,  step=1)
        data[f'SMA2 {period2}'] = data['Adj Close'].rolling(period2).mean()
        data2[f'SMA2 {period2}'] = data[f'SMA2 {period2}'].reindex(data2.index)

    st.subheader('Chart')
    st.line_chart(data2)

    if st.sidebar.checkbox('View basic stats'):
        st.subheader('Stats')
        st.table(data2.describe())

    if st.sidebar.checkbox('View quotes'):
        st.subheader(f'{asset} historical data')
        st.write(data2)
        st.sidebar.subheader("""Display Additional Information""")
    # checkbox to display stock actions for the searched ticker
    actions = st.sidebar.checkbox("Stock Actions")
    if actions:
        st.subheader("""Stock **actions** for """ + selected_stock)
        display_action = (stock_data.actions)
        if display_action.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_action)
    
    # checkbox to display quarterly financials for the searched ticker
    financials = st.sidebar.checkbox("Quarterly Financials")
    if financials:
        st.subheader("""**Quarterly financials** for """ + selected_stock)
        display_financials = (stock_data.quarterly_financials)
        if display_financials.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_financials)

    # checkbox to display list of institutional shareholders for searched ticker
    major_shareholders = st.sidebar.checkbox("Institutional Shareholders")
    if major_shareholders:
        st.subheader("""**Institutional investors** for """ + selected_stock)
        display_shareholders = (stock_data.institutional_holders)
        if display_shareholders.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_shareholders)

    # checkbox to display quarterly balance sheet for searched ticker
    balance_sheet = st.sidebar.checkbox("Quarterly Balance Sheet")
    if balance_sheet:
        st.subheader("""**Quarterly balance sheet** for """ + selected_stock)
        display_balancesheet = (stock_data.quarterly_balance_sheet)
        if display_balancesheet.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_balancesheet)

    # checkbox to display quarterly cashflow for searched ticker
    cashflow = st.sidebar.checkbox("Quarterly Cashflow")
    if cashflow:
        st.subheader("""**Quarterly cashflow** for """ + selected_stock)
        display_cashflow = (stock_data.quarterly_cashflow)
        if display_cashflow.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_cashflow)

    # checkbox to display quarterly earnings for searched ticker
    earnings = st.sidebar.checkbox("Quarterly Earnings")
    if earnings:
        st.subheader("""**Quarterly earnings** for """ + selected_stock)
        display_earnings = (stock_data.quarterly_earnings)
        if display_earnings.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_earnings)

    # checkbox to display list of analysts recommendation for searched ticker
    analyst_recommendation = st.sidebar.checkbox("Analysts Recommendation")
    if analyst_recommendation:
        st.subheader("""**Analysts recommendation** for """ + selected_stock)
        display_analyst_rec = (stock_data.recommendations)
        if display_analyst_rec.empty == True:
            st.write("No data available at the moment")
        else:
            st.write(display_analyst_rec)

    st.sidebar.title("About")
    st.sidebar.info('This app is a simple interactive financial dashboard, created for Data Visualization course of Artificial Intelligence degree at the Poznań University of Technology.')
