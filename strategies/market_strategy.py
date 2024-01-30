import pandas as pd
from strategies.abstract_strategy import POStrategy
class MarketStrategy(POStrategy):
    # In the market strategy, you want to keep your weights always synchronized with the relative market capitalization rel_cap = market_cap / sum(market_caps)
    # market_cap = price * outstanding_shares
    # If you keep your number (amount) of shares per asset constant,
    # since  I. price * amount = value
    # and   II. weight = value / sum(value) = rel_value
    #       ->  weight = price*amount / sum(price*amount) = rel_value
    # comparing with
    #           market_cap = price*outstanding_shares
    #       ->  price*outstanding_shares / sum(market_caps) = rel_cap
    # we see that with 'amount' and 'outstanding_shares' const., a change in price will change 'rel_value' and 'rel_cap' equally.
    # Therefore, we only need to set the 'amount' we choose to buy initially according to the market proportion and the remainder is also only Buy-and-Hold.
    def __init__(self, market_caps: pd.Series):
        # how can you retrieve the market capitalization? It is not visible in the price dataframe. you need to pass it
        # market_caps can be a Series with absolute market caps
        self.init_market_caps = market_caps
        self.amounts = None

    def decision_making(self, known_price_history):
        # also in Market, we do not rebalance
        # this means the target weights just equal the market value ratios, so that we do not buy or sell anything
        # in other words, the amount of each asset we hold remains the same
        if len(known_price_history.index) == 0:
            assert len(self.init_market_caps) == len(
                known_price_history.columns), 'the intialized market caps must equal the price history asset dim in size'
            n_assets = len(self.init_market_caps)  # init according to market caps
            target_weights = self.init_market_caps / self.init_market_caps.sum()
            self.init_relative_portf_value = 1
        else:
            # the remainder stays similar as in UBAH
            curr_prices = known_price_history.iloc[-1]  # series
            if self.amounts is None:  # derive the amount of each asset we could buy initally
                init_weights = self.init_market_caps / self.init_market_caps.sum()
                target_allocation = self.init_relative_portf_value * init_weights
                self.amounts = target_allocation / curr_prices  # then later reuse the self.amounts

            # derive the new weights so that they equal the weights that are implied anyway for the current prices
            self.relative_market_values = curr_prices * self.amounts
            current_weights = self.relative_market_values / self.relative_market_values.sum()
            target_weights = current_weights
        return target_weights