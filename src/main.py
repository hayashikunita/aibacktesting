import os
from scripts.yahoofinance2csv import fetch_and_save_stock
from strategies import SimpleStrategy
import sys
sys.path.append('../tools')  # toolsディレクトリをパスに追加
from tools.ai_optimize_strategy import optimize_strategy_with_ai
from data import Backtesterdata
from backtest import Backtester
from utils import calculate_performance

def main():
    # 日本株データの読み込み（例: 東証のCSV形式、日付・終値・始値・高値・安値・出来高など）
    # data = Backtesterdata.load_japan_stock_data('src/data/japan_stock.csv')
    # data = Backtesterdata.load_japan_stock_data('src\data\japan_stock.csv')

    symbolplusT = "2267.T"  # デフォルトシンボル
    print(f"使用するシンボル: {symbolplusT}")
    yn = input("このシンボルで進めますか？ (y/n): ").strip().lower()
    if yn == 'n':
        symbol = input("新しいシンボルを入力してください（例: 2267）: ").strip()
        if not symbol.endswith('.T'):
            symbol += '.T'
            symbolplusT = symbol
        else:
            symbolplusT = symbol
        print(f"使用するシンボル: {symbolplusT}")

    file_name = f"japan_stock_{symbolplusT}.csv"
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", file_name))
    # os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    if not os.path.exists(csv_path):
        fetch_and_save_stock(symbol, csv_path)
    else:
        print(f"既存のCSVファイルを使用します: {csv_path}")

    data = Backtesterdata.load_japan_stock_data(csv_path)

    # 戦略の初期化（日本株は取引時間や祝日などに注意）
    # strategy = SimpleStrategy(data, short_window=100, long_window=200)
    strategy = SimpleStrategy(data, short_window=5, long_window=25)

    # バックテストの実行
    backtester = Backtester(strategy, data)
    results = backtester.run(initial_cash=1000000)  # 初期資金100万円

    # 売買ごとのリターン（利益率）・損益額リストを作成
    trade_returns = []
    trade_profits = []
    trade_log = results['trade_log']
    for i in range(len(trade_log)):
        trade = trade_log[i]
        if trade['type'] == 'sell':
            entry_trade = trade_log[i-1] if i > 0 else None
            if entry_trade and entry_trade['type'] == 'buy':
                entry_price = entry_trade['price']
                exit_price = trade['price']
                profit = exit_price - entry_price
                ret = profit / entry_price
                trade_returns.append(ret)
                trade_profits.append(profit)

    import numpy as np
    performance = calculate_performance(np.array(trade_returns), np.array(trade_profits))

    # AIによる戦略パラメータ最適化案の表示
    backtest_result = {
        "final_cash": float(results['final_cash']),
        "performance": performance,
        "strategy": strategy,
    }
    api_key = "YOUR_API_KEY"  # 必要に応じて環境変数等で管理してください
    try:
        ai_suggestion = optimize_strategy_with_ai(backtest_result, api_key)
        print("\n--- AIによる最適化案 ---")
        print(ai_suggestion)
    except Exception as e:
        print("AI最適化案の取得に失敗しました:", e)
    
    # 結果の表示
    # print("日本株バックテスト結果:", results)


# ...existing code...
    print("トレード履歴:")
    for trade in results['trade_log']:
        if trade['type'] == 'buy':
            print(f"  買い: 価格={float(trade['price'])} index={trade['index']}")
        elif trade['type'] == 'sell':
            print(f"  売り: 価格={float(trade['price'])} index={trade['index']} 利益={float(trade['profit'])}")
# ...existing code...

    # print("パフォーマンス指標:", performance)

# ...existing code...
    # 結果の表示
    print("日本株バックテスト結果（最終資金）:", float(results['final_cash']))
    # print("トレード履歴:", results['trade_log'])
    print("パフォーマンス指標:")
    for k, v in performance.items():
        print(f"  {k}: {float(v):.4%}" if 'return' in k or 'volatility' in k else f"  {k}: {float(v):.4f}")
# ...existing code...

if __name__ == "__main__":
    main()