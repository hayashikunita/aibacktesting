# import pandas as pd

# def calculate_performance(returns):
#     # numpy配列の場合はpandas.Seriesに変換
#     if not isinstance(returns, pd.Series):
#         returns = pd.Series(returns)
#     cumulative_return = (1 + returns).prod() - 1
#     annualized_return = (1 + cumulative_return) ** (252 / len(returns)) - 1
#     volatility = returns.std() * (252 ** 0.5)
#     sharpe_ratio = annualized_return / volatility if volatility != 0 else 0

#     num_trades = len(returns)
#     wins = returns[returns > 0]
#     losses = returns[returns < 0]
#     win_rate = len(wins) / num_trades if num_trades > 0 else 0
#     avg_win = wins.mean() if len(wins) > 0 else 0
#     avg_loss = losses.mean() if len(losses) > 0 else 0
#     expected_value = win_rate * avg_win + (1 - win_rate) * avg_loss

#     # 最大ドローダウン
#     cumulative = (1 + returns).cumprod()
#     peak = cumulative.cummax()
#     drawdown = (cumulative - peak) / peak
#     max_drawdown = drawdown.min() if len(drawdown) > 0 else 0

#     # プロフィットファクター（総利益/総損失）
#     gross_profit = wins.sum() if len(wins) > 0 else 0
#     gross_loss = abs(losses.sum()) if len(losses) > 0 else 0
#     profit_factor = gross_profit / gross_loss if gross_loss != 0 else float('inf')

#     # ペイオフレシオ（平均利益/平均損失）
#     payoff_ratio = avg_win / abs(avg_loss) if avg_loss != 0 else float('inf')

#     # リスクリワードレシオ（期待値/平均損失）
#     risk_reward_ratio = expected_value / abs(avg_loss) if avg_loss != 0 else float('inf')

#     # 連勝・連敗数
#     win_streak = 0
#     max_win_streak = 0
#     loss_streak = 0
#     max_loss_streak = 0
#     for r in returns:
#         if r > 0:
#             win_streak += 1
#             loss_streak = 0
#         elif r < 0:
#             loss_streak += 1
#             win_streak = 0
#         else:
#             win_streak = 0
#             loss_streak = 0
#         max_win_streak = max(max_win_streak, win_streak)
#         max_loss_streak = max(max_loss_streak, loss_streak)

#     return {
#         '累積リターン': cumulative_return,
#         '年率リターン': annualized_return,
#         'ボラティリティ': volatility,
#         'シャープレシオ': sharpe_ratio,
#         '勝率': win_rate,
#         '期待値（1トレード）': expected_value,
#         '平均利益': avg_win,
#         '平均損失': avg_loss,
#         'トレード回数': num_trades,
#         '最大ドローダウン': max_drawdown,
#         'プロフィットファクター': profit_factor,
#         'ペイオフレシオ': payoff_ratio,
#         'リスクリワードレシオ': risk_reward_ratio,
#         '最大連勝数': max_win_streak,
#         '最大連敗数': max_loss_streak
#     }

# # 日本語で分かりやすく表示する関数
# def print_performance(perf):
#     print("\nパフォーマンス指標:")
#     for k, v in perf.items():
#         if k in ['累積リターン', '年率リターン', 'ボラティリティ', '勝率', '最大ドローダウン']:
#             print(f"  {k}: {v*100:.2f}%")
#         elif k in ['平均利益', '平均損失', '期待値（1トレード）']:
#             print(f"  {k}: {v*100:.4f}%")
#         elif k in ['トレード回数', '最大連勝数', '最大連敗数']:
#             print(f"  {k}: {v:.0f} 回")
#         else:
#             print(f"  {k}: {v:.4f}")

import pandas as pd

def calculate_performance(returns, profits=None):
    # numpy配列の場合はpandas.Seriesに変換
    if not isinstance(returns, pd.Series):
        returns = pd.Series(returns)
    if profits is not None and not isinstance(profits, pd.Series):
        profits = pd.Series(profits)

    cumulative_return = (1 + returns).prod() - 1
    annualized_return = (1 + cumulative_return) ** (252 / len(returns)) - 1
    volatility = returns.std() * (252 ** 0.5)
    sharpe_ratio = annualized_return / volatility if volatility != 0 else 0

    num_trades = len(returns)
    wins = returns[returns > 0]
    losses = returns[returns < 0]
    win_rate = len(wins) / num_trades if num_trades > 0 else 0
    avg_win = wins.mean() if len(wins) > 0 else 0
    avg_loss = losses.mean() if len(losses) > 0 else 0
    expected_value = win_rate * avg_win + (1 - win_rate) * avg_loss

    # 金額ベースの計算
    if profits is not None:
        wins_amt = profits[profits > 0]
        losses_amt = profits[profits < 0]
        avg_win_amt = wins_amt.mean() if len(wins_amt) > 0 else 0
        avg_loss_amt = losses_amt.mean() if len(losses_amt) > 0 else 0
        expected_value_amt = win_rate * avg_win_amt + (1 - win_rate) * avg_loss_amt
    else:
        avg_win_amt = None
        avg_loss_amt = None
        expected_value_amt = None

    # 最大ドローダウン
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min() if len(drawdown) > 0 else 0

    # プロフィットファクター（総利益/総損失）
    gross_profit = wins.sum() if len(wins) > 0 else 0
    gross_loss = abs(losses.sum()) if len(losses) > 0 else 0
    profit_factor = gross_profit / gross_loss if gross_loss != 0 else float('inf')

    # ペイオフレシオ（平均利益/平均損失）
    payoff_ratio = avg_win / abs(avg_loss) if avg_loss != 0 else float('inf')

    # リスクリワードレシオ（期待値/平均損失）
    risk_reward_ratio = expected_value / abs(avg_loss) if avg_loss != 0 else float('inf')

    # 連勝・連敗数
    win_streak = 0
    max_win_streak = 0
    loss_streak = 0
    max_loss_streak = 0
    for r in returns:
        if r > 0:
            win_streak += 1
            loss_streak = 0
        elif r < 0:
            loss_streak += 1
            win_streak = 0
        else:
            win_streak = 0
            loss_streak = 0
        max_win_streak = max(max_win_streak, win_streak)
        max_loss_streak = max(max_loss_streak, loss_streak)

    return {
        '累積リターン': cumulative_return,
        '年率リターン': annualized_return,
        'ボラティリティ': volatility,
        'シャープレシオ': sharpe_ratio,
        '勝率': win_rate,
        '期待値（1トレード・%）': expected_value,
        '期待値（1トレード・金額）': expected_value_amt,
        '平均利益（%）': avg_win,
        '平均損失（%）': avg_loss,
        '平均利益（円）': avg_win_amt,
        '平均損失（円）': avg_loss_amt,
        'トレード回数': num_trades,
        '最大ドローダウン': max_drawdown,
        'プロフィットファクター': profit_factor,
        'ペイオフレシオ': payoff_ratio,
        'リスクリワードレシオ': risk_reward_ratio,
        '最大連勝数': max_win_streak,
        '最大連敗数': max_loss_streak
    }

def print_performance(perf):
    print("\nパフォーマンス指標:")
    for k, v in perf.items():
        if k in ['累積リターン', '年率リターン', 'ボラティリティ', '勝率', '最大ドローダウン']:
            print(f"  {k}: {v*100:.2f}%")
        elif k in ['平均利益（%）', '平均損失（%）', '期待値（1トレード・%）']:
            print(f"  {k}: {v*100:.4f}%")
        elif k in ['平均利益（円）', '平均損失（円）', '期待値（1トレード・金額）']:
            print(f"  {k}: {v:.2f} 円")
        elif k in ['トレード回数', '最大連勝数', '最大連敗数']:
            print(f"  {k}: {v:.0f} 回")
        else:
            print(f"  {k}: {v:.4f}")