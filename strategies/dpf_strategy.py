
import pandas as pd
import numpy as np
from strategies.abstract_strategy import POStrategyYoung

def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class DPFStrategy(POStrategyYoung):
    def __init__(self):
        self.amounts = None
        self.initial_prices = None
        self.daily_amounts = []  # 初始化一个列表来存储每天的投资量

    def decision_making(self, known_price_history):
        curr_prices = known_price_history.iloc[-1]
        if self.amounts is None:
            # 初始投资，等额分配
            self.amounts = 1 / curr_prices
            self.initial_prices = curr_prices

        # 计算价格变化百分比
        price_change_percentage = (curr_prices - self.initial_prices) / self.initial_prices
        # 调整权重：价格下降更多的资产获得更高的权重增加
        adjustment_factor = 12  # factor 调整因子，可以根据需要进行调整
        weights = 1 - adjustment_factor * price_change_percentage

        weights = 1 - adjustment_factor * price_change_percentage
        weights[price_change_percentage > 0] = weights[price_change_percentage > 0] - 0.2
        weights[price_change_percentage < 0] = weights[price_change_percentage < 0] + 0.2

        # 将sigmoid函数应用到weights的每个元素
        # or do this
        # weights = price_change_percentage.apply(sigmoid)

        weights = np.maximum(weights, 0.001)

        # 标准化权重，使其总和为1
        weights /= weights.sum()
        self.daily_amounts.append(self.amounts.copy())
        # 根据新权重计算投资量
        total_investment = np.dot(self.amounts, self.initial_prices)

        self.amounts = weights * total_investment / curr_prices
        # 更新价格
        self.initial_prices = curr_prices

        return weights