import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyfolio


def plot_cov_mat(covmat_df, fmt='.2g'):
    plt.figure(figsize=(10, 8))
    sns.heatmap(covmat_df, annot=True, fmt=fmt, cmap='coolwarm')
    plt.title('Covariance Matrix Heatmap')
    plt.show()


"""Columns: assets, Rows: Dates"""


def plot_prices_relative(prices_df):
    plt.figure(figsize=(10, 6))
    plt.plot(prices_df / prices_df.iloc[0], linestyle='-', label=prices_df.columns)
    plt.title('Stock Performance Over Time')
    plt.xlabel('Date')
    plt.ylabel('Relative Price')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_df(df, title=''):
    plt.figure(figsize=(10, 6))
    plt.plot(df, linestyle='-', label=df.columns)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('')
    plt.grid(True)
    plt.legend()
    plt.show()

class GeometricBrownianMotion:
    def __init__(self, S0, mu, sigma):
        """
        Initialize the parameters of the GBM.
        :param S0: Initial stock price
        :param mu: Drift coefficient
        :param sigma: Volatility coefficient
        """
        self.S0 = S0
        self.mu = mu
        self.sigma = sigma

    def generate_series(self, T, steps=None):
        """
        Generate a GBM series.
        :param T: Total time period
        :param steps: Number of steps in the time period
        :return: A numpy array representing the GBM series
        """
        if steps is None: steps = T
        dt = T / steps
        t = np.linspace(0, T, steps)
        W = np.random.standard_normal(size=steps)
        W = np.cumsum(W) * np.sqrt(dt)  # Cumulative sum to simulate Brownian Motion
        S = self.S0 * np.exp((self.mu - 0.5 * self.sigma ** 2) * t + self.sigma * W)
        return S

# Example of using the class
# gbm = GeometricBrownianMotion(S0=100, mu=0.05, sigma=0.2)
# series = gbm.generate_series(T=100)

class Market:
    def __init__(self):
        self.assets = list()

    def list_(self, asset):
        self.assets.append(asset)

    def mcap(self):
        return sum(ass.p * ass.m for ass in self.assets)


class Asset:
    def __init__(self, shares_outstanding, price, name=''):
        self.m = shares_outstanding
        self.p = price
        self.name = name

    def fetch_price(self):
        return p  # yfTicker.history(period='1d')['Close'][-1]

    @classmethod
    def fromYFinance(cls, yfTicker):
        m = yfTicker.info.get('sharesOutstanding')
        p = yfTicker.history(period='1d')['Close'][-1]
        n = yfTicker.info.get('longName')
        return cls(m, p, n)

    def mcap(self):
        return self.m * self.p


class Position:
    def __init__(self, asset, amount):
        self.asset = asset
        self.amount = amount

    def value(self):
        return self.amount * self.asset.p


class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.positions = list()

    def buy(self, stock, amount):
        self.cash -= stock.p * amount
        self.positions += [Position(stock, amount)]

    def total_value(self):
        return sum(ass.value() for ass in self.positions)

    def summary(self):
        # Create a DataFrame to show each asset's name, price, and total value (assuming quantity is part of positions)
        data = {
            'Asset': [position.asset.name for position in self.positions],
            'Price': [position.asset.p for position in self.positions],
            'Value': [position.asset.p * position.amount for position in self.positions]
            # Assumes each position has a 'quantity' attribute
        }
        df = pd.DataFrame(data)
        df.loc[len(df.index)] = ['Cash', '', self.cash]  # Add total cash
        df.loc[len(df.index)] = ['Total Value', '', self.total_value()]  # Add total value
        return df

def accumulate_returns(returns):
    """Input: Dataframe with returns like p(t)/p(t-1)-p(t-1)"""
    cumm_returns = [1,]
    for ret in stock_rets:
        cumm_returns.append(cumm_returns[-1] * (1+ret))
    cumm_returns = pd.DataFrame(index=stock_rets.index, data=cumm_returns[1:], columns=[stock_rets.name])
    return cumm_returns

def calc_CW(t_c_df): # rows time, columns assets
    return t_c_df.iloc[-1,:] / t_c_df.iloc[0,:]

def calc_APY(t_c_df, years_covered):
    return calc_CW(t_c_df) ** (1/years_covered) - 1 # convert

def calc_MDD(t_c_df): # rows time, columns assets
    return pyfolio.timeseries.max_drawdown(t_c_df.pct_change())  # max draw down is expressed as negative -> also the larger the better

def calc_SR(t_c_df): # rows time, columns assets
    return pd.Series(pyfolio.timeseries.sharpe_ratio(t_c_df.pct_change()),index=t_c_df.columns, name='SR')

def calc_AVO(t_c_df):
    return pd.Series(pyfolio.timeseries.annual_volatility(t_c_df.pct_change()),index=t_c_df.columns, name='AVO')

def calc_APYAVOMDD(t_c_df, years_covered=1):
    return calc_APY(t_c_df, years_covered), calc_AVO(t_c_df), calc_MDD(t_c_df)

def calc_CWMDDSR(t_c_df):
    return calc_CW(t_c_df), calc_MDD(t_c_df), calc_SR(t_c_df)