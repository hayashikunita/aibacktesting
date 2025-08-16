
import yfinance as yf
import pandas as pd
import os

def fetch_and_save_stock(symbol, csv_path):
	# ヤフーファイナンスから株価データを取得
	df = yf.download(symbol, period="max", interval="1d")
	if df.empty:
		print(f"データが取得できませんでした: {symbol}")
		return False
	# 日付を列として保存
	df.reset_index(inplace=True)
	df.to_csv(csv_path, index=False)
	print(f"CSVファイルを保存しました: {csv_path}")
	return True

# if __name__ == "__main__":
# 	# 2267はヤクルト本社の証券コード
# 	symbol = "2267.T"  # Yahoo!ファイナンスの日本株は末尾に .T
# 	csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "japan_stock.csv"))
# 	os.makedirs(os.path.dirname(csv_path), exist_ok=True)
# 	fetch_and_save_stock(symbol, csv_path)
