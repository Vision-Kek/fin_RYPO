import pandas as pd
from strategies.abstract_strategy import POStrategyYoung

class MeanReversionStrategy(POStrategyYoung):
    def __init__(self, lookback_period=30):
        self.amounts = None
        self.daily_amounts = []  # 用于存储每日的amounts
        self.lookback_period = lookback_period

    def decision_making(self, known_price_history):
        current_prices = known_price_history.iloc[-1]

        if len(known_price_history) < self.lookback_period:
            # 当数据点少于lookback_period时，使用等权重策略
            weights = np.ones(len(known_price_history.columns)) / len(known_price_history.columns)
        else:
            historical_avg = known_price_history[-self.lookback_period:].mean()
            deviation_from_mean = current_prices - historical_avg
            weights = 1 / (1 + np.exp(deviation_from_mean))  # use a sigmoid function

        weights /= weights.sum()

        # 无论是否达到lookback_period，都需要更新amounts
        if self.amounts is None:
            self.amounts = np.ones(len(weights)) / current_prices
        else:
            total_investment = np.dot(self.amounts, current_prices)
            self.amounts = weights * total_investment / current_prices

        self.daily_amounts.append(self.amounts.copy())

        return weights