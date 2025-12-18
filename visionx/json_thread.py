"""
Serial JSON reader thread: reads newline JSON from ESP32 or stdin (mock).
Pushes dicts to an output queue.
"""

import threading
import time
import json
import re
import sys
from queue import Queue

from .config import SER_PORTS, SER_BAUD

_JSON_RE = re.compile(r"\{.*\}")

try:
    import serial
except Exception:
    serial = None

class SerialJSONReader(threading.Thread):
    def __init__(self, out_queue: Queue, ports=None, baud=None, timeout=1.0, mock=False, mock_stream=None):
        super().__init__(daemon=True)
        self.out_queue = out_queue
        self.ports = ports or SER_PORTS
        self.baud = baud or SER_BAUD
        self.timeout = timeout
        self.mock = mock
        self.mock_stream = mock_stream or sys.stdin
        self._running = threading.Event()
        self._running.set()
        self._ser = None

    def _open_serial(self):
        if serial is None:
            return False
        for p in self.ports:
            try:
                self._ser = serial.Serial(p, self.baud, timeout=self.timeout)
                print(f"[json_thread] opened serial {p} @ {self.baud}")
                return True
            except Exception:
                continue
        return False

    def stop(self):
        self._running.clear()
        try:
            if self._ser and self._ser.is_open:
                self._ser.close()
        except Exception:
            pass

    def run(self):
        if self.mock:
            self._run_mock()
            return

        ok = self._open_serial()
        if ok:
            self._run_serial()
        else:
            print("[json_thread] no serial ports opened; falling back to mock/stdin")
            self._run_mock()

    def _run_serial(self):
        while self._running.is_set():
            try:
                raw = self._ser.readline().decode(errors="ignore").strip()
            except Exception:
                raw = ""
            if not raw:
                time.sleep(0.01)
                continue
            self._try_parse_push(raw)

    def _run_mock(self):
        while self._running.is_set():
            try:
                raw = self.mock_stream.readline()
            except Exception:
                time.sleep(0.05)
                continue
            if raw == "":
                time.sleep(0.05)
                continue
            raw = raw.strip()
            if not raw:
                continue
            self._try_parse_push(raw)

    def _try_parse_push(self, raw_line: str):
        m = _JSON_RE.search(raw_line)
        if not m:
            return
        try:
            obj = json.loads(m.group())
            obj['_ts'] = time.time()
            self.out_queue.put(obj)
        except Exception:
            return
