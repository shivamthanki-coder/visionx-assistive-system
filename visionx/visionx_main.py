"""
Main orchestrator: wires serial -> detection -> tts -> logging.
"""

import argparse
import time
from queue import Queue, Empty
from pathlib import Path

from .config import FRAME_STRIDE, PERSON_HITS_REQUIRED, SAVE_INTERVAL_SEC, OUT_DIR, LOG_FILE, CAMERA_SIZE
from .json_thread import SerialJSONReader
from .tts_queue import TTSQueue
from . import detection
from .utils import now_ts, append_jsonl, ensure_dir, safe_get

ensure_dir(OUT_DIR)

def setup_camera_or_none():
    try:
        from picamera2 import Picamera2
        picam2 = Picamera2()
        config = picam2.create_video_configuration(main={"size": CAMERA_SIZE, "format": "BGR888"})
        picam2.configure(config)
        picam2.start()
        picam2.set_controls({"FrameRate": 30})
        return picam2
    except Exception as exc:
        print("[visionx_main] camera unavailable:", exc)
        return None

def main(mock_serial=False):
    serial_q = Queue()
    serial_reader = SerialJSONReader(out_queue=serial_q, mock=mock_serial)
    serial_reader.start()

    tts = TTSQueue()
    picam2 = setup_camera_or_none()
    have_camera = picam2 is not None

    latest_dist_m = None
    latest_gps = "no fix"
    person_hits = 0
    last_speech = 0
    last_save = 0
    frame_id = 0

    try:
        while True:
            # consume serial messages
            while True:
                try:
                    obj = serial_q.get_nowait()
                except Empty:
                    break
                dvals = []
                for k in ("d1_cm", "d2_cm"):
                    v = obj.get(k)
                    if isinstance(v, (int, float)) and v > 0:
                        dvals.append(v / 100.0)
                if dvals:
                    latest_dist_m = min(dvals)
                lat = safe_get(obj, ("lat",))
                lng = safe_get(obj, ("lng",))
                sats = safe_get(obj, ("sats",))
                if lat is not None and lng is not None:
                    latest_gps = f"{lat:.6f}, {lng:.6f}, sats={sats}"
                else:
                    latest_gps = "no fix"

            # capture frame
            if have_camera:
                frame = picam2.capture_array()
            else:
                import numpy as np
                frame = (np.zeros((CAMERA_SIZE[1], CAMERA_SIZE[0], 3), dtype="uint8"))

            frame_id += 1
            if frame_id % FRAME_STRIDE != 0:
                time.sleep(0.01)
                continue

            detections = []
            try:
                detections = detection.detect(frame)
            except Exception:
                detections = []

            best_label, best_conf = None, 0.0
            for d in detections:
                label = d.get("label")
                conf = float(d.get("conf", 0.0))
                if label == "person" and conf >= best_conf:
                    best_label, best_conf = label, conf
                elif best_label is None and conf >= best_conf:
                    best_label, best_conf = label, conf

            now = time.time()
            if best_label and (now - last_save) >= SAVE_INTERVAL_SEC:
                try:
                    import cv2
                    cv2.imwrite(str(Path(OUT_DIR) / "latest_obj.jpg"), frame)
                    last_save = now
                except Exception:
                    pass

            if best_label == "person":
                person_hits = min(person_hits + 1, 5)
            else:
                person_hits = max(person_hits - 1, 0)

            if person_hits >= PERSON_HITS_REQUIRED and latest_dist_m and (now - last_speech) >= 2.0:
                spoken = f"Person ahead, {latest_dist_m:.1f} meters"
                tts.enqueue(spoken, priority=100, dedupe_key="person_ahead")
                last_speech = now
                event = {
                    "ts": now_ts(),
                    "event": "person",
                    "conf": best_conf,
                    "dist_m": latest_dist_m,
                    "gps": latest_gps,
                    "tts": spoken
                }
                append_jsonl(LOG_FILE, event)

            time.sleep(0.03)

    except KeyboardInterrupt:
        print("[visionx_main] interrupted")
    finally:
        serial_reader.stop()
        tts.stop()
        print("[visionx_main] shutdown complete")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock-serial", action="store_true", help="read JSON from stdin instead of real serial")
    args = parser.parse_args()
    main(mock_serial=args.mock_serial)
