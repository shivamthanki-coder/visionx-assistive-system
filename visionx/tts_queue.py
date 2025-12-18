"""
Prioritized, deduplicating TTS queue.
Use enqueue(text, priority=int, dedupe_key=str)
"""

import threading
import time
import heapq
import uuid
import subprocess

from .config import TTS_DEDUPE_SEC, TTS_QUEUE_MAX, TTS_RATE, TTS_VOICE

_SPEAK_CMD = 'espeak-ng -s {rate} -v {voice} "{text}" --stdout | aplay >/dev/null 2>&1'

class TTSQueue:
    def __init__(self, max_size=None, dedupe_window=None, rate=None, voice=None):
        self.max_size = max_size or TTS_QUEUE_MAX
        self.dedupe_window = dedupe_window or TTS_DEDUPE_SEC
        self.rate = rate or TTS_RATE
        self.voice = voice or TTS_VOICE

        self._lock = threading.Lock()
        self._heap = []  # (-priority, ts, uid, text, dedupe_key)
        self._last_spoken = {}
        self._stop = threading.Event()
        self._worker = threading.Thread(target=self._worker_loop, name="tts-worker", daemon=True)
        self._worker.start()

    def enqueue(self, text, priority=50, dedupe_key=None):
        now = time.time()
        if dedupe_key is None:
            dedupe_key = text

        last = self._last_spoken.get(dedupe_key)
        if last and (now - last) < self.dedupe_window:
            return False

        with self._lock:
            if len(self._heap) >= self.max_size:
                current = [(-p, ts, uid, t, key) for (p, ts, uid, t, key) in self._heap]
                lowest_priority = min(current, key=lambda e: e[0])[0]
                if priority <= lowest_priority:
                    return False
                removed = False
                new_heap = []
                for (p, ts, uid, t, key) in self._heap:
                    if not removed and (-p) == lowest_priority:
                        removed = True
                        continue
                    new_heap.append((p, ts, uid, t, key))
                heapq.heapify(new_heap)
                self._heap = new_heap

            uid = uuid.uuid4().hex
            heapq.heappush(self._heap, (-priority, now, uid, text, dedupe_key))
            return True

    def _pop(self):
        with self._lock:
            if not self._heap:
                return None
            p, ts, uid, text, dedupe_key = heapq.heappop(self._heap)
            return -p, ts, uid, text, dedupe_key

    def _worker_loop(self):
        while not self._stop.is_set():
            item = self._pop()
            if item is None:
                time.sleep(0.05)
                continue
            priority, ts, uid, text, dedupe_key = item
            try:
                cmd = _SPEAK_CMD.format(rate=self.rate, voice=self.voice, text=text.replace('"', "'"))
                subprocess.run(cmd, shell=True, check=False)
            except Exception:
                pass
            self._last_spoken[dedupe_key] = time.time()

    def stop(self, wait=True):
        self._stop.set()
        if wait:
            self._worker.join(timeout=2.0)
