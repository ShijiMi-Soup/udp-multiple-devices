# OSC サーバーとプログレスバーのチュートリアル

複数のデバイスからOSCメッセージを受信し、プログレスバーで可視化するチュートリアルです。

## ファイル

- **1_base_server.py** - 基本的なOSCサーバー
- **2_async_server.py** - 非同期OSCサーバー（複数ポート対応）
- **3_progressbar.py** - プログレスバー付きOSCサーバー
- **test_osc_sender.py** - テスト用メッセージ送信スクリプト
- **TUTORIAL_JA.md** - 詳細なチュートリアル

## 使い方

```bash
# 依存パッケージをインストール
pip install -r requirements.txt

# プログレスバーサーバーを起動
python 3_progressbar.py

# 別のターミナルでテストスクリプトを実行
python test_osc_sender.py
```

詳しい説明は [TUTORIAL_JA.md](./TUTORIAL_JA.md) をご覧ください。

