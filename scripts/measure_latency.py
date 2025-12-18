#!/usr/bin/env python3
import time
import numpy as np
from visionx import detection
from visionx.tts_queue import TTSQueue

def measure_inference(num=20):
    img = np.zeros((320,320,3), dtype="uint8")
    times = []
    for _ in range(num):
        t0 = time.time()
        _ = detection.detect(img)
        times.append(time.time() - t0)
    return times

def measure_tts(tts, messages=3):
    start = time.time()
    for i in range(messages):
        tts.enqueue(f"Latency test {i+1}", priority=10, dedupe_key=f"lat_{i}")
    while True:
        if time.time() - start > 30:
            break
        heap = getattr(tts, "_heap", None)
        if heap is None or not heap:
            break
        time.sleep(0.2)
    return time.time() - start

if __name__ == "__main__":
    print("Measuring inference...")
    t = measure_inference(10)
    print("avg inf (s):", sum(t)/len(t))
    tts = TTSQueue()
    print("Measuring TTS...")
    elapsed = measure_tts(tts, messages=2)
    print("TTS elapsed:", elapsed)
    tts.stop()
