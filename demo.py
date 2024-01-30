
import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import fintools.finance_tools as finutils
import strategies
from fintools.valuing import calc_portfolio_value_from_weights, infer_amounts

def getClosePrices(stocks, start, end):
    stockData =yf.download(stocks, start=start, end=end)
    stockData = stockData['Close']
    stockData = stockData.dropna(axis=1, subset=[stockData.index[0], stockData.index[-1]], how='any') # drop values that do not have first or last entry
    stockData = stockData.interpolate()# interpolate inbetween
    return stockData

def demo_ubah():
    tickers = ['AAPL', 'MSFT']  # this is the 'asset pool' we choose to evaluate on
    stockData_test = getClosePrices(tickers, start=dt.datetime(2021, 1, 1),
                                    end=dt.datetime(2022, 1, 1))  # this is the time frame we choose to evaluate on

    ubah = strategies.ubah_strategy.UBAHStrategy()
    ubah_weights = ubah.run(stockData_test)

    # this method is only valid for ubah
    value_development_jisuan_fangfa1 = stockData_test.multiply(ubah.amounts)
    # this is the general way to do it!
    value_development_jisuan_fangfa2, ubah_amounts = calc_portfolio_value_from_weights(stockData_test, ubah_weights)
    display(ubah_amounts)

    print('ubah value_development')
    value_development_jisuan_fangfa1['sum'] = value_development_jisuan_fangfa1.sum(axis=1)  # check if they're equal
    value_development_jisuan_fangfa2['sum'] = value_development_jisuan_fangfa2.sum(axis=1)  # check if they're equal

    display(value_development_jisuan_fangfa1)
    display(value_development_jisuan_fangfa2)

    print('ubah weights')
    ubah_weights['sum'] = ubah_weights.sum(axis=1)
    display(ubah_weights)

    finutils.plot_df(ubah_weights, title='UBAH_WEIGHTS')
    finutils.plot_df(value_development_jisuan_fangfa1, title='ubah portfolio value calc-method 1')
    finutils.plot_df(value_development_jisuan_fangfa2, title='ubah portfolio value calc-method 2')

def demo_market():
    tickers = ['AAPL', 'MSFT']  # this is the 'asset pool' we choose to evaluate on
    stockData_test = getClosePrices(tickers, start=dt.datetime(2021, 1, 1),
                                    end=dt.datetime(2022, 1, 1))  # this is the time frame we choose to evaluate on
    market_caps = pd.Series([yf.Ticker(t).info.get('marketCap') for t in tickers], index=stockData_test.columns)

    marketstrat = strategies.market_strategy.MarketStrategy(market_caps)

    weights = marketstrat.run(stockData_test)
    values, _ = calc_portfolio_value_from_weights(stockData_test, weights)

    finutils.plot_df(weights, title='MARKET_SRAT_WEIGHTS')
    finutils.plot_df(values, title='MARKET_STRAT_VALUES')

def demo_dpf():
    tickers = ['AAPL', 'MSFT']  # this is the 'asset pool' we choose to evaluate on
    stockData_test = getClosePrices(tickers, start=dt.datetime(2021, 1, 1),
                                    end=dt.datetime(2022, 1, 1))  # this is the time frame we choose to evaluate on

    dpfstrat = strategies.dpf_strategy.DPFStrategy()

    weights = dpfstrat.run(stockData_test)
    values, _ = calc_portfolio_value_from_weights(stockData_test, weights)

    finutils.plot_df(weights, title='DPF_SRAT_WEIGHTS')
    finutils.plot_df(values, title='DPF_STRAT_VALUES')

def demo_mean_reversion():
    tickers = ['AAPL', 'MSFT']  # this is the 'asset pool' we choose to evaluate on
    stockData_test = getClosePrices(tickers, start=dt.datetime(2021, 1, 1),
                                    end=dt.datetime(2022, 1, 1))  # this is the time frame we choose to evaluate on

    meanrevstrat = strategies.meanrev_strategy.MeanReversionStrategy()

    weights = meanrevstrat.run(stockData_test)
    values, _ = calc_portfolio_value_from_weights(stockData_test, weights)

    finutils.plot_df(weights, title='MEAN_REV_SRAT_WEIGHTS')
    finutils.plot_df(values, title='MEAN_REV_SRAT_VALUES')