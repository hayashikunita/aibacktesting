import pandas as pd

class Backtesterdata:
    @staticmethod
    def load_japan_stock_data(filepath):
        """
        日本株CSVデータを読み込む関数
        必要なカラム: date, open, high, low, close, volume
        """
        df = pd.read_csv(filepath, skiprows=[1], parse_dates=['Date'])
        # 列名を小文字化
        df = df.rename(columns={
            'Date': 'date',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        })
        # 必要なカラムのみ抽出
        df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
        # 数値型に変換
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    # @staticmethod
    # def load_japan_stock_data(filepath):
    #     """
    #     日本株CSVデータを読み込む関数
    #     必要なカラム: DateTime, Open, High, Low, Close, Volume
    #     """
    #     df = pd.read_csv(filepath, parse_dates=['DateTime'])
    #     # 列名を統一（小文字化）
    #     df = df.rename(columns={
    #         'DateTime': 'date',
    #         'Open': 'open',
    #         'High': 'high',
    #         'Low': 'low',
    #         'Close': 'close',
    #         'Volume': 'volume'
    #     })
    #     return df

