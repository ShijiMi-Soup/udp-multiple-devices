"""
OSCサーバーのテストスクリプト

このスクリプトは、OSCサーバー（3_progressbar.py）にランダムな値を送信して
プログレスバーの動作を確認するためのものです。

使用方法：
1. 別のターミナルで `python 3_progressbar.py` を実行
2. このスクリプトを実行: `python test_osc_sender.py`
3. プログレスバーが更新されることを確認
"""

from pythonosc import udp_client
import time
import random

# 設定
IP = "127.0.0.1"
PORTS = [8000, 8001]

# クライアントの作成
clients = [
    udp_client.SimpleUDPClient(IP, port) for port in PORTS
]

print(f"OSCクライアントを起動しました。")
print(f"送信先: {IP} ポート: {PORTS}")
print("Ctrl+Cで終了します。\n")

# ランダムな値を送信
try:
    while True:
        for i, client in enumerate(clients):
            # 0から100までのランダムな値を生成
            attention = random.uniform(0, 100)
            meditation = random.uniform(0, 100)
            
            # OSCメッセージを送信
            client.send_message('/Attention', attention)
            client.send_message('/Meditation', meditation)
            
            print(f"ポート {PORTS[i]}: Attention={attention:.1f}, Meditation={meditation:.1f}")
        
        print()  # 空行
        time.sleep(0.5)  # 0.5秒待機
        
except KeyboardInterrupt:
    print("\n\n終了します")
