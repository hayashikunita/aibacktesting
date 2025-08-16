
import openai
import json
import os

def optimize_strategy_with_ai(backtest_result, api_key=None, model="gpt-4"):
    """
    バックテスト結果をもとに、SimpleStrategyのパラメータ最適化案と
    書き換えPythonコードをChatGPTから取得する関数
    api_keyは引数または環境変数OPENAI_API_KEYから取得可能
    """
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI APIキーが指定されていません。引数または環境変数OPENAI_API_KEYを設定してください。")

    prompt = f"""
        以下は日本株バックテストの結果です。
        {json.dumps(backtest_result, ensure_ascii=False, indent=2)}
        この結果をもとに、SimpleStrategyのStrategyのPythonコードを、さらに良くするPythonコードを出力してください。
        """
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "あなたは優秀なPythonエンジニアです。"},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"OpenAI APIリクエストでエラーが発生しました: {e}"

# テスト用サンプル（必要なら有効化）
# if __name__ == "__main__":
#     backtest_result = {
#         "final_cash": 1350000,
#         "performance": {
#             "cumulative_return": 0.35,
#             "annual_return": 0.12,
#             "max_drawdown": -0.08,
#             "win_rate": 0.55
#         },
#         "current_short_window": 100,
#         "current_long_window": 200
#     }
#     result = optimize_strategy_with_ai(backtest_result)
#     print(result)