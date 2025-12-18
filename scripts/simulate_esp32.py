#!/usr/bin/env python3
"""
ESP32 JSON simulator for dev/testing.
Usage:
  python3 scripts/simulate_esp32.py | python3 -m visionx.visionx_main --mock-serial
"""
import time, json, random, sys

def make_msg():
    d1 = round(random.uniform(80, 250), 1)  # cm
    lat = round(23.18 + random.uniform(-0.02, 0.02), 6)
    lng = round(72.62 + random.uniform(-0.02, 0.02), 6)
    sats = random.randint(0, 12)
    return {"d1_cm": d1, "lat": lat, "lng": lng, "sats": sats}

if __name__ == "__main__":
    while True:
        msg = make_msg()
        sys.stdout.write(json.dumps(msg) + "\\n")
        sys.stdout.flush()
        time.sleep(0.5)
