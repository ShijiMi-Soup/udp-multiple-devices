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


# 関数 =========================

def handler(address, *args):
    print(f"{address}: {args}")


# アドレスと関数を紐付け 
disp = Dispatcher()
for address in addresses:
    disp.map(address, handler)

# メインの処理 =========================

def create_osc_server(ip, port, dispatcher, loop):
    server =  AsyncIOOSCUDPServer((ip, port), dispatcher, loop)
    print(f"ポート {port} でOSCサーバーを作成しました。")
    return server

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

if __name__ == "__main__":
    asyncio.run(main())
