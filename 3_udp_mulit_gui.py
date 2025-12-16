import sys, time
from collections import deque

from PySide6 import QtCore, QtWidgets
import pyqtgraph as pg

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer


class OscWorker(QtCore.QObject):
    message = QtCore.Signal(int, str, float, float)

    def __init__(self, configs):
        super().__init__()
        self.configs = configs
        self.servers = []
        self.threads = []

    def _dispatcher(self, port, routes):
        disp = Dispatcher()

        def handler(address, *args):
            if not args:
                return
            try:
                v = float(args[0])
            except (TypeError, ValueError):
                return
            self.message.emit(port, address, v, time.time())

        for r in routes:
            disp.map(r, handler)
        return disp

    @QtCore.Slot()
    def start(self):
        for ip, port, routes in self.configs:
            disp = self._dispatcher(port, routes)
            server = ThreadingOSCUDPServer((ip, port), disp)
            self.servers.append(server)

            t = QtCore.QThread()
            self.threads.append(t)

            runner = QtCore.QObject()
            runner.moveToThread(t)

            def run():
                server.serve_forever()

            t.started.connect(run)
            t.start()

    @QtCore.Slot()
    def stop(self):
        for s in self.servers:
            try:
                s.shutdown()
                s.server_close()
            except Exception:
                pass
        for t in self.threads:
            t.quit()
            t.wait(1000)

        self.servers.clear()
        self.threads.clear()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OSC Monitor (PySide6 + pyqtgraph)")

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        self.plot = pg.PlotWidget()
        layout.addWidget(self.plot)
        self.curve_9000 = self.plot.plot()
        self.curve_9001 = self.plot.plot()

        row = QtWidgets.QHBoxLayout()
        self.start_btn = QtWidgets.QPushButton("Start")
        self.stop_btn = QtWidgets.QPushButton("Stop")
        self.stop_btn.setEnabled(False)
        row.addWidget(self.start_btn)
        row.addWidget(self.stop_btn)
        layout.addLayout(row)

        self.buf0 = deque(maxlen=500)
        self.buf1 = deque(maxlen=500)

        self.worker = OscWorker([
            ("0.0.0.0", 9000, ["/a"]),
            ("0.0.0.0", 9001, ["/b"]),
        ])
        self.worker.message.connect(self.on_msg)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(33)
        self.timer.timeout.connect(self.refresh)

        self.start_btn.clicked.connect(self.start)
        self.stop_btn.clicked.connect(self.stop)

    @QtCore.Slot()
    def start(self):
        self.worker.start()
        self.timer.start()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    @QtCore.Slot()
    def stop(self):
        self.timer.stop()
        self.worker.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    @QtCore.Slot(int, str, float, float)
    def on_msg(self, port, address, value, ts):
        if port == 9000:
            self.buf0.append(value)
        elif port == 9001:
            self.buf1.append(value)

    @QtCore.Slot()
    def refresh(self):
        self.curve_9000.setData(list(self.buf0))
        self.curve_9001.setData(list(self.buf1))

    def closeEvent(self, event):
        self.stop()
        super().closeEvent(event)


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.resize(900, 500)
w.show()
sys.exit(app.exec())
