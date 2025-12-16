from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

# 設定 =========================

IP = "127.0.0.1"
PORT = 8000

addresses = [
    "/Attention",
    "/Meditation"
]


# 関数 =========================

def handler(address, *args):
    print(f"{address}: {args}")


# メインの処理 =========================

# アドレスと関数を紐付け 
disp = Dispatcher()
for address in addresses:
    disp.map(address, handler)

# サーバーを起動
print(f"OSCサーバ (ポート: {PORT}) ... Ctrl-Cで終了")
server = ThreadingOSCUDPServer((IP, PORT), disp) # サーバーの作成
server.serve_forever() # サーバーを起動（Ctrl+Cで終了）
