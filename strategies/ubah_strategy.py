import pandas as pd
from strategies.abstract_strategy import POStrategy
class UBAHStrategy(POStrategy):  # Uniform Buy and Hold
    def __init__(self):
        self.amounts = None
        self.weights = None

    # override
    def decision_making(self, known_price_history):
        # in UBAH, we buy uniformly, but then do not rebalance
        # this means the target weights just equal the market value ratios, so that we do not buy or sell anything
        # in other words, the amount of each asset we hold remains the same
        if len(known_price_history.index) == 0:
            n_assets = len(known_price_history.columns)  # init uniformly
            self.weights = pd.Series([1 / n_assets] * n_assets, index=known_price_history.columns)
            self.init_relative_portf_value = 1
        else:
            curr_prices = known_price_history.iloc[-1].to_numpy()
            if self.amounts is None:  # derive the amount of each asset we could buy initally
                target_allocation = self.init_relative_portf_value * self.weights
                self.amounts = target_allocation / curr_prices  # then later reuse the self.amounts

            # derive the new weights so that they equal the weights that are implied anyway for the current prices
            self.relative_market_values = curr_prices * self.amounts
            current_weights = self.relative_market_values / self.relative_market_values.sum()
            self.weights = current_weights
        return self.weights