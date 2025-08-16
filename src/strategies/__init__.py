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

__all__ = ['SimpleStrategy']