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

# 設定 =========================
IP = "127.0.0.1"
PORTS = [8000, 8001]

# 表示する値の最大値
PROGRESS_MAX = 100.0

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

            # ハンドラー関数を作成する関数
            def make_handler(task_id: TaskID):
                # ハンドラー関数
                def _handler(address: str, *args):
                    if not args:
                        return

                    progress.update(task_id, completed=args[0])
                
                # 作成した関数を返す
                return _handler

            # ディスパッチャに関数を登録
            disp.map("/Attention", make_handler(attention_task))
            disp.map("/Meditation", make_handler(meditation_task))

            # サーバーを起動
            server = AsyncIOOSCUDPServer((IP, port), disp, loop)
            servers.append(server)

        print(f"Listening on {IP} ports: {PORTS}")

        # 後でUDP通信を閉じるためのオブジェクト
        endpoints = [await s.create_serve_endpoint() for s in servers]

        try:
            # Ctrl+C まで待機
            await asyncio.Event().wait()
        finally:
            for transport, _ in endpoints:
                transport.close()


if __name__ == "__main__":
    asyncio.run(main())
