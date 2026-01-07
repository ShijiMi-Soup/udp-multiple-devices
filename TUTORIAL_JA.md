# OSCサーバーとプログレスバーの実装チュートリアル

このチュートリアルでは、OSC（Open Sound Control）サーバーを使用してデータを受信し、プログレスバーで可視化する方法を段階的に学習します。

## 目次

1. [はじめに](#1-はじめに)
2. [環境構築](#2-環境構築)
3. [基本的なOSCサーバー（1_base_server.py）](#3-基本的なoscサーバー1_base_serverpy)
4. [非同期OSCサーバー（2_async_server.py）](#4-非同期oscサーバー2_async_serverpy)
5. [プログレスバーの実装（3_progressbar.py）](#5-プログレスバーの実装3_progressbarpy)
6. [動作確認](#6-動作確認)

---

## 1. はじめに

### OSC（Open Sound Control）とは？

OSCは、音楽やマルチメディアアプリケーション間でリアルタイムにデータを送受信するためのプロトコルです。MIDIよりも柔軟で高速なデータ通信が可能です。

### このプロジェクトの目的

このプロジェクトでは、複数のデバイスからOSCメッセージを受信し、それぞれのデータをプログレスバーで可視化します。具体的には：

- **Attention（集中度）**
- **Meditation（瞑想度）**

これらの値を受信して、リアルタイムで表示します。

---

## 2. 環境構築

### 必要なパッケージのインストール

まず、必要なPythonパッケージをインストールします。

```bash
pip install -r requirements.txt
```

`requirements.txt`の内容：
```
rich
python-osc
```

- **python-osc**: OSC通信を扱うためのライブラリ
- **rich**: ターミナルに美しいプログレスバーを表示するためのライブラリ

---

## 3. 基本的なOSCサーバー（1_base_server.py）

### 概要

最初のステップでは、シンプルなOSCサーバーを作成します。このサーバーは1つのポートでOSCメッセージを受信し、コンソールに表示します。

### コードの解説

```python
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

# 設定 =========================

IP = "127.0.0.1"
PORT = 8000

addresses = [
    "/Attention",
    "/Meditation"
]
```

**設定部分の説明：**
- `IP`: サーバーがリッスンするIPアドレス（ローカルホスト）
- `PORT`: サーバーがリッスンするポート番号
- `addresses`: 受信するOSCアドレスのリスト

```python
# 関数 =========================

def handler(address, *args):
    print(f"{address}: {args}")
```

**ハンドラー関数：**
- OSCメッセージを受信したときに呼び出される関数
- `address`: OSCアドレス（例："/Attention"）
- `*args`: 受信したデータ（可変長引数）

```python
# メインの処理 =========================

# アドレスと関数を紐付け 
disp = Dispatcher()
for address in addresses:
    disp.map(address, handler)

# サーバーを起動
print(f"OSCサーバ (ポート: {PORT}) ... Ctrl-Cで終了")
server = ThreadingOSCUDPServer((IP, PORT), disp) # サーバーの作成
server.serve_forever() # サーバーを起動（Ctrl+Cで終了）
```

**メイン処理の説明：**
1. `Dispatcher`を作成：OSCアドレスとハンドラー関数を紐付けるオブジェクト
2. 各アドレスに対してハンドラー関数を登録
3. `ThreadingOSCUDPServer`を作成：スレッドベースのUDPサーバー
4. `serve_forever()`でサーバーを起動（Ctrl+Cで終了）

### 実行方法

```bash
python 1_base_server.py
```

### 動作確認

別のターミナルで以下のコマンドを使ってOSCメッセージを送信できます：

```bash
# python-oscがインストールされている場合
python -c "from pythonosc import udp_client; client = udp_client.SimpleUDPClient('127.0.0.1', 8000); client.send_message('/Attention', 75.5)"
```

---

## 4. 非同期OSCサーバー（2_async_server.py）

### 概要

次のステップでは、複数のポートで同時にOSCメッセージを受信できる非同期サーバーを作成します。これにより、複数のデバイスからのデータを同時に処理できます。

### 同期サーバーと非同期サーバーの違い

- **同期サーバー（ThreadingOSCUDPServer）**: 1つのポートのみ
- **非同期サーバー（AsyncIOOSCUDPServer）**: 複数のポートを同時に処理可能

### コードの解説

```python
import asyncio
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer

# 設定 =========================

IP = "127.0.0.1"
PORTS = [8000, 8001]

addresses = [
    "/Attention",
    "/Meditation"
]
```

**設定の変更点：**
- `PORT`（単数）から`PORTS`（複数）に変更
- 複数のポート番号をリストで定義

```python
# 関数 =========================

def handler(address, *args):
    print(f"{address}: {args}")

# アドレスと関数を紐付け 
disp = Dispatcher()
for address in addresses:
    disp.map(address, handler)
```

**ハンドラーとディスパッチャー：**
- 基本的なサーバーと同じ構造
- ただし、すべてのサーバーで共有される

```python
# メインの処理 =========================

def create_osc_server(ip, port, dispatcher, loop):
    server =  AsyncIOOSCUDPServer((ip, port), dispatcher, loop)
    print(f"ポート {port} でOSCサーバーを作成しました。")
    return server
```

**サーバー作成関数：**
- 各ポートに対してOSCサーバーを作成
- `AsyncIOOSCUDPServer`を使用（非同期版）
- `loop`パラメータで非同期イベントループを指定

```python
async def main():
    loop = asyncio.get_running_loop()
    assert isinstance(loop, asyncio.BaseEventLoop)

    servers = [
        create_osc_server(IP, port, disp, loop) for port in PORTS
    ]

    endpoints = [
        await server.create_serve_endpoint() for server in servers
    ]

    try:
        await asyncio.Event().wait() # 待機
    finally:
        for endpoint in endpoints:
            transport, _ = endpoint
            transport.close()
```

**非同期メイン関数：**
1. `asyncio.get_running_loop()`で現在の非同期イベントループを取得
2. リスト内包表記で各ポートにサーバーを作成
3. `create_serve_endpoint()`で各サーバーのエンドポイントを作成（実際に通信開始）
4. `asyncio.Event().wait()`で無限に待機（Ctrl+Cまで）
5. 終了時にすべてのトランスポートをクローズ

```python
if __name__ == "__main__":
    asyncio.run(main())
```

**プログラムの起動：**
- `asyncio.run()`で非同期メイン関数を実行

### 実行方法

```bash
python 2_async_server.py
```

### 動作確認

複数のポートにメッセージを送信して確認：

```bash
# ポート8000に送信
python -c "from pythonosc import udp_client; client = udp_client.SimpleUDPClient('127.0.0.1', 8000); client.send_message('/Attention', 75.5)"

# ポート8001に送信
python -c "from pythonosc import udp_client; client = udp_client.SimpleUDPClient('127.0.0.1', 8001); client.send_message('/Meditation', 82.3)"
```

---

## 5. プログレスバーの実装（3_progressbar.py）

### 概要

最終ステップでは、受信したOSCデータをプログレスバーで可視化します。`rich`ライブラリを使用して、美しく見やすいプログレスバーを実装します。

### 新しい機能

- 各ポート・各アドレスごとに独立したプログレスバーを表示
- リアルタイムでプログレスバーを更新
- 値の範囲は0〜100

### コードの解説

```python
import asyncio
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer

from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TaskProgressColumn,
    TaskID
)
from rich.text import Text
```

**インポート：**
- `rich.progress`から必要なコンポーネントをインポート
  - `Progress`: プログレスバーのメインクラス
  - `BarColumn`: プログレスバーの表示
  - `TextColumn`: テキスト表示
  - `TaskProgressColumn`: 進捗率の表示
  - `TaskID`: タスクの識別子

```python
# 設定 =========================
IP = "127.0.0.1"
PORTS = [8000, 8001]

# 表示する値の最大値
PROGRESS_MAX = 100.0
```

**設定：**
- `PROGRESS_MAX`: プログレスバーの最大値（0〜100）

```python
async def main():
    loop = asyncio.get_running_loop()

    # プログレスバーを作成
    progress = Progress(
        TextColumn("[bold]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("{task.completed:>6.1f} / {task.total:.0f}"),
        refresh_per_second=20,
        transient=False,
    )
```

**Progressオブジェクトの作成：**
- `TextColumn("[bold]{task.description}")`: タスク名を太字で表示
- `BarColumn()`: プログレスバーを表示
- `TaskProgressColumn()`: パーセンテージを表示
- `TextColumn("{task.completed:>6.1f} / {task.total:.0f}")`: 現在値/最大値を表示
- `refresh_per_second=20`: 1秒間に20回更新
- `transient=False`: プログラムが終了してもプログレスバーを残す

```python
    # プログレスバーを描画
    with progress:
        # OSCサーバーを入れるリスト
        servers = []

        # ポートごとにディスパッチャとタスクを作成し、サーバーを起動
        for port in PORTS:
            # ディスパッチャーを作成
            disp = Dispatcher()

            # タスクを作成（attention, meditation) 
            attention_task = progress.add_task(f"{port}: Attention", total=PROGRESS_MAX)
            meditation_task = progress.add_task(f"{port} Meditation", total=PROGRESS_MAX)
```

**プログレスバーのセットアップ：**
1. `with progress:`でプログレスバーのコンテキストを開始
2. 各ポートごとに：
   - 新しい`Dispatcher`を作成（ポートごとに独立したディスパッチャー）
   - Attentionとメディテーション用のタスクを作成
   - `progress.add_task()`で新しいプログレスバーを追加

```python
            # ハンドラー関数を作成する関数
            def make_handler(task_id: TaskID):
                # ハンドラー関数
                def _handler(address: str, *args):
                    if not args:
                        return

                    progress.update(task_id, completed=args[0])
                
                # 作成した関数を返す
                return _handler
```

**ハンドラー関数のファクトリー：**
- `make_handler(task_id)`: クロージャを使用してハンドラーを生成
- 各タスクIDに対応したハンドラーを作成
- `_handler(address, *args)`: 実際のハンドラー関数
  - 引数がない場合は何もしない
  - `progress.update(task_id, completed=args[0])`で進捗を更新

**クロージャを使う理由：**
- 各ポート・各アドレスごとに異なるタスクIDを持つハンドラーが必要
- `make_handler()`を使うことで、task_idを保持したハンドラーを生成できる

```python
            # ディスパッチャに関数を登録
            disp.map("/Attention", make_handler(attention_task))
            disp.map("/Meditation", make_handler(meditation_task))

            # サーバーを起動
            server = AsyncIOOSCUDPServer((IP, port), disp, loop)
            servers.append(server)
```

**ディスパッチャーとサーバーの設定：**
1. 各OSCアドレスに対応するハンドラーを登録
2. 非同期OSCサーバーを作成
3. サーバーをリストに追加

```python
        print(f"Listening on {IP} ports: {PORTS}")

        # 後でUDP通信を閉じるためのオブジェクト
        endpoints = [await s.create_serve_endpoint() for s in servers]

        try:
            # Ctrl+C まで待機
            await asyncio.Event().wait()
        finally:
            for transport, _ in endpoints:
                transport.close()
```

**サーバーの起動と待機：**
1. すべてのサーバーのエンドポイントを作成
2. 無限に待機（Ctrl+Cまで）
3. 終了時にすべてのトランスポートをクローズ

```python
if __name__ == "__main__":
    asyncio.run(main())
```

### 実行方法

```bash
python 3_progressbar.py
```

### 期待される出力

```
Listening on 127.0.0.1 ports: [8000, 8001]
8000: Attention    ████████░░░░░░░░░░░░   40.0%   40.0 / 100
8000  Meditation   ███████████████░░░░░   75.0%   75.0 / 100
8001: Attention    ████████████░░░░░░░░   60.0%   60.0 / 100
8001  Meditation   ██████████████████░░   90.0%   90.0 / 100
```

---

## 6. 動作確認

### テストスクリプトの作成

プログレスバーをテストするためのスクリプトを作成します。

```python
# test_osc_sender.py
from pythonosc import udp_client
import time
import random

# クライアントの作成
clients = [
    udp_client.SimpleUDPClient('127.0.0.1', 8000),
    udp_client.SimpleUDPClient('127.0.0.1', 8001),
]

# ランダムな値を送信
try:
    while True:
        for i, client in enumerate(clients):
            attention = random.uniform(0, 100)
            meditation = random.uniform(0, 100)
            
            client.send_message('/Attention', attention)
            client.send_message('/Meditation', meditation)
            
            print(f"ポート {8000+i}: Attention={attention:.1f}, Meditation={meditation:.1f}")
        
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\n終了します")
```

### 実行手順

1. まず、プログレスバーのサーバーを起動：
```bash
python 3_progressbar.py
```

2. 別のターミナルでテストスクリプトを実行：
```bash
python test_osc_sender.py
```

3. プログレスバーがリアルタイムで更新されることを確認

---

## まとめ

このチュートリアルでは、以下の内容を学習しました：

### 1. 基本的なOSCサーバー（1_base_server.py）
- OSCの基本概念
- `ThreadingOSCUDPServer`を使った単一ポートのサーバー
- ディスパッチャーとハンドラーの関係

### 2. 非同期OSCサーバー（2_async_server.py）
- 非同期プログラミングの基礎
- `AsyncIOOSCUDPServer`を使った複数ポートのサーバー
- `asyncio`による非同期処理

### 3. プログレスバーの実装（3_progressbar.py）
- `rich`ライブラリによる美しいUIの作成
- クロージャを使った動的なハンドラーの生成
- リアルタイムデータの可視化

### 発展課題

- より多くのポートとアドレスに対応
- データのログ記録機能を追加
- グラフィカルUIの実装（4_udp_mulit_gui.pyを参照）
- データのフィルタリングやスムージング

---

## トラブルシューティング

### ポートが既に使用されている

```
OSError: [Errno 98] Address already in use
```

**解決方法：**
```bash
# 使用中のポートを確認
lsof -i :8000

# プロセスを終了
kill -9 <PID>
```

### パッケージが見つからない

```
ModuleNotFoundError: No module named 'pythonosc'
```

**解決方法：**
```bash
pip install python-osc rich
```

### メッセージが受信されない

1. ファイアウォールの設定を確認
2. IPアドレスとポート番号が正しいか確認
3. サーバーが起動しているか確認

---

## 参考リンク

- [python-osc Documentation](https://python-osc.readthedocs.io/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [OSC Specification](http://opensoundcontrol.org/)
- [Python asyncio](https://docs.python.org/ja/3/library/asyncio.html)
