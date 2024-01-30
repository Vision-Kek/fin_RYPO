import pandas as pd
class POStrategy:
    def __init__(self):
        pass

    # OVERRIDE THIS METHOD IN YOUR STRATEGY
    # BUT DO NOT CALL IT DIRECTLY, CALL run() INSTEAD
    # input: known_price_history: [days,assets]
    def decision_making(self, known_price_history):
        weights = None
        return weights  # series

    # CALL THIS
    # input: price_df: [days,assets]
    def run(self, price_df):
        weights = price_df.copy()  # [days,assets]
        for d in range(
                len(price_df.index)):  # every day, based on the known (previous) price history, make a new decision
            # at time t=d...
            known_history = price_df.iloc[:d]
            weights_decided = self.decision_making(known_history)
            weights.iloc[d] = weights_decided

        return weights  # [days,assets]


class POStrategyYoung:
    def __init__(self):
        pass

    # OVERRIDE THIS METHOD IN YOUR STRATEGY
    # BUT DO NOT CALL IT DIRECTLY, CALL run() INSTEAD
    # input: known_price_history: [days,assets]
    def decision_making(self, known_price_history):
        weights = None
        return weights  # series

    # CALL THIS
    # input: price_df: [days,assets]
    def run(self, price_df):
        weights = price_df.copy()  # [days,assets]
        for d in range(1, len(price_df.index) + 1):  # every day, based on the known (previous)
            # ----price history, make a new decision
            # at time t=d...
            known_history = price_df.iloc[:d]
            weights_decided = self.decision_making(known_history)
            weights.iloc[d - 1] = weights_decided

        return weights  # [days,assets]