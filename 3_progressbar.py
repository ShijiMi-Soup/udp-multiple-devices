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

    # ディスパッチャーを作成
    disp = Dispatcher()

    # プログレスバーを描画
    with progress:
        # 各データ (attention, meditation) ごとのタスクを作成
        attention_task = progress.add_task("Attention", total=PROGRESS_MAX)
        meditation_task = progress.add_task("Meditation", total=PROGRESS_MAX)

        # プログレスバーの数値を更新する関数
        def update_task(task_id: TaskID, *args):
            if not args:
                return
            progress.update(task_id, completed=args[0])

        # アドレスと関数を紐付け
        disp.map("/Attention", lambda address, *args: update_task(attention_task, *args))
        disp.map("/Meditation", lambda address, *args: update_task(meditation_task, *args))

        # 複数ポートで OSC サーバーを起動
        servers = [
            AsyncIOOSCUDPServer((IP, port), disp, loop) for port in PORTS
        ]
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
