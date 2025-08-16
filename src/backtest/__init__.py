class Backtester:
    def __init__(self, strategy, data):
        self.strategy = strategy
        self.data = data

    def run(self, initial_cash=1000000):
        df = self.strategy.execute()
        cash = initial_cash
        position = 0  # 0: ノーポジ, 1: ロング
        entry_price = 0
        trade_log = []
        equity_curve = [initial_cash] * len(df)

        for i, (idx, row) in enumerate(df.iterrows()):
            # Update equity based on current position and price
            if position == 1:
                equity_curve[i] = cash + (row['close'] - entry_price)
            else:
                equity_curve[i] = cash

            if row['position'] == 1 and position == 0:
                # Buy signal
                position = 1
                entry_price = row['close']
                trade_log.append({'type': 'buy', 'price': entry_price, 'index': idx})
            elif row['position'] == -1 and position == 1:
                # Sell signal
                exit_price = row['close']
                profit = exit_price - entry_price
                cash += profit
                position = 0
                trade_log.append({'type': 'sell', 'price': exit_price, 'index': idx, 'profit': profit})
                equity_curve[i] = cash  # Update equity after closing position

        df['equity'] = equity_curve
        df['returns'] = df['equity'].pct_change().fillna(0)

        return {'final_cash': cash, 'trade_log': trade_log, 'df': df, 'returns': df['returns']}