#!/usr/bin/env python3
import time
import os
from visionx.tts_queue import TTSQueue

def run_test():
    dry = os.environ.get("DRY_RUN") == "1"
    tts = TTSQueue()
    tts.enqueue("Low priority", priority=10, dedupe_key="p_low")
    tts.enqueue("High priority", priority=100, dedupe_key="p_high")
    time.sleep(0.2)
    tts.enqueue("Low duplicate", priority=10, dedupe_key="dup")
    time.sleep(0.1)
    tts.enqueue("Low duplicate", priority=10, dedupe_key="dup")
    time.sleep(5)
    tts.stop()
    print("TTSQueue test done")

if __name__ == "__main__":
    run_test()
