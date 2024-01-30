# Parameters:
# weights:         a Series of Size [assets]
# portfolio_value: int
# current_prices:  a Series of Size [assets]
# Returns:         a Series of Size [assets]
def infer_amounts(weights, portfolio_value, current_prices):
    assert np.isclose(weights.sum(), 1), f'weights must sum to 1, got {weights}'
    target_allocation = portfolio_value * weights
    assert np.isclose(target_allocation.sum(),
                      portfolio_value), f'init_allocation must sum to init_portfolio_value {target_allocation=},{portfolio_value=}'
    inferred_amounts = target_allocation / current_prices
    return inferred_amounts


# Parameters:
# stockData: price dataframes [time x asset]
# weights:   time dataframes [time x asset]
# Returns:
# values_we_hold: value dataframe [time x asset]
# amounts_we_hold: amount dataframe [time x asset]
def calc_portfolio_value_from_weights(stockData, weights):
    assert (np.isclose(weights.sum(axis=1), 1)).all, f'weights must sum to 1, got {weights}'
    assert (len(stockData.index) == len(weights.index)), 'you must provide weights for every time stamp'
    assert (len(stockData.columns) == len(weights.columns)), 'you must provide weights for every asset'
    T, A = len(stockData.index), len(stockData.columns)
    # --------------------
    # these two dataframes [time x asset] we want to fill
    amounts_we_hold = pd.DataFrame(columns=stockData.columns)
    values_we_hold = pd.DataFrame(columns=stockData.columns)
    # --------------------
    # for t=0:
    # assuming we start with portfolio_value = 1 (we only care about relative performance)
    init_portfolio_value = 1
    init_prices = stockData.iloc[0]
    init_weights = weights.iloc[0]
    # calculate the corresponding amount we can can hold for each asset
    amounts_we_hold.loc[0] = infer_amounts(init_weights, init_portfolio_value, init_prices)  # Series for t=0
    values_we_hold.loc[0] = amounts_we_hold.loc[0] * init_prices  # Series for t=0
    assert np.isclose(values_we_hold.loc[0].sum(), init_portfolio_value), 'error'

    # for all further t=1, t=2, ..., t=T
    for t in range(1, T):
        current_prices = stockData.iloc[t]  # read
        inferred_position_values = amounts_we_hold.loc[
                                       t - 1] * current_prices  # derive: new portfolio value, given the new prices
        target_weights = weights.iloc[t]  # read
        amounts_we_hold.loc[t] = infer_amounts(target_weights, inferred_position_values.sum(),
                                               current_prices)  # update (rebalancing given target_weights)
        values_we_hold.loc[t] = amounts_we_hold.loc[t] * current_prices  # derive
        assert np.isclose(inferred_position_values.sum(),
                          values_we_hold.loc[t].sum()), 'the portfolio value does not change through rebalancing'

    return values_we_hold, amounts_we_hold