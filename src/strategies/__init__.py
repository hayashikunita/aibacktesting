import pandas as pd

class SimpleStrategy:
    # この SimpleStrategy クラスは、移動平均線（SMA）を使ったシンプルな売買ストラテジーです。

    # short_window（デフォルト5）とlong_window（デフォルト20）の2つの期間でSMA（単純移動平均）を計算します。
    # 株価データ（close）に対して、短期SMAと長期SMAを算出します。
    # 短期SMAが長期SMAを上回った場合に「買いシグナル」（signal=1）、それ以外は「売りシグナル」（signal=0）となります。
    # シグナルの変化（position）で売買タイミングを判定します。position=1は買い、position=-1は売りのタイミングです。
    # つまり、ゴールデンクロス（短期線が長期線を上抜け）で買い、デッドクロス（短期線が長期線を下抜け）で売る、という典型的な移動平均クロスオーバー戦略です。

    def __init__(self, data, short_window=50, long_window=300):
        self.data = data
        self.short_window = short_window
        self.long_window = long_window

    def execute(self):
        df = pd.DataFrame(self.data)
        df['short_sma'] = df['close'].rolling(window=self.short_window).mean()
        df['long_sma'] = df['close'].rolling(window=self.long_window).mean()
        df['signal'] = 0
        condition = df['short_sma'] > df['long_sma']
        df.loc[self.short_window:, 'signal'] = condition[self.short_window:].astype(int)

        df['position'] = df['signal'].diff()
        # position: 1=買いシグナル, -1=売りシグナル
        return df[['close', 'short_sma', 'long_sma', 'signal', 'position']]

class RSIStrategy:
    # RSI（Relative Strength Index）を使ったシンプルな売買ストラテジー
    # period（デフォルト14）でRSIを計算し、30未満で買い、70超で売りシグナルを出します。
    def __init__(self, data, period=14, buy_threshold=30, sell_threshold=70):
        self.data = data
        self.period = period
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def execute(self):
        df = pd.DataFrame(self.data)
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=self.period, min_periods=self.period).mean()
        avg_loss = loss.rolling(window=self.period, min_periods=self.period).mean()
        rs = avg_gain / avg_loss
        df['rsi'] = 100 - (100 / (1 + rs))
        df['signal'] = 0
        df.loc[df['rsi'] < self.buy_threshold, 'signal'] = 1
        df.loc[df['rsi'] > self.sell_threshold, 'signal'] = -1
        df['position'] = df['signal'].diff()
        # position: 1=買いシグナル, -1=売りシグナル
        return df[['close', 'rsi', 'signal', 'position']]

class MACDStrategy:
    # MACD（移動平均収束拡散法）を使ったシンプルな売買ストラテジー
    # 短期EMA（デフォルト12）、長期EMA（デフォルト26）、シグナル線（デフォルト9）
    # MACDがシグナル線を上抜けたら買い、下抜けたら売りシグナル
    def __init__(self, data, short_period=12, long_period=26, signal_period=9):
        self.data = data
        self.short_period = short_period
        self.long_period = long_period
        self.signal_period = signal_period

    def execute(self):
        df = pd.DataFrame(self.data)
        df['ema_short'] = df['close'].ewm(span=self.short_period, adjust=False).mean()
        df['ema_long'] = df['close'].ewm(span=self.long_period, adjust=False).mean()
        df['macd'] = df['ema_short'] - df['ema_long']
        df['macd_signal'] = df['macd'].ewm(span=self.signal_period, adjust=False).mean()
        df['signal'] = 0
        df.loc[df['macd'] > df['macd_signal'], 'signal'] = 1
        df.loc[df['macd'] < df['macd_signal'], 'signal'] = -1
        df['position'] = df['signal'].diff()
        # position: 1=買いシグナル, -1=売りシグナル
        return df[['close', 'macd', 'macd_signal', 'signal', 'position']]

__all__ = ['SimpleStrategy', 'RSIStrategy', 'MACDStrategy']