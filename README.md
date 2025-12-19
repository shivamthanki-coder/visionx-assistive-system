# VisionX — Wearable Assistive Vision System

VisionX is a modular, real-time assistive system designed to help visually impaired users perceive nearby obstacles using computer vision, proximity sensing, and audio feedback.

The system combines YOLO-based object detection, ultrasonic distance sensing, and a prioritized text-to-speech (TTS) pipeline, engineered to run headlessly on a Raspberry Pi with an ESP32 acting as a sensor reflex unit.

--------------------------------------------------------------------------------
KEY FEATURES
--------------------------------------------------------------------------------

- Real-time object detection using YOLOv3-tiny (edge-optimized)
- Sensor fusion: camera vision + ultrasonic distance + optional GPS
- Non-blocking, prioritized TTS queue with deduplication
- Hardware-mockable pipeline for development without physical devices
- Cross-platform development (macOS / Linux) with Raspberry Pi deployment
- Structured logging for evaluation, debugging, and metrics
- Systemd-ready for auto-start on boot

--------------------------------------------------------------------------------
SYSTEM ARCHITECTURE (HIGH LEVEL)
--------------------------------------------------------------------------------
<pre>
ESP32 (Ultrasonic + GPS)
        |
        |  JSON over Serial (USB)
        v
Raspberry Pi (VisionX Core)
  |- Picamera2 -> YOLO Detection
  |- Alert Logic + Debounce
  |- Priority TTS Queue
  `- Structured Event Logging
        |
        v
Bluetooth Earbuds (Audio Feedback)
</pre>
--------------------------------------------------------------------------------
REPOSITORY STRUCTURE
--------------------------------------------------------------------------------

<pre>
visionx-assistive-system/
├── visionx/
│   ├── visionx_main.py
│   ├── detection.py
│   ├── json_thread.py
│   ├── tts_queue.py
│   ├── config.py
│   └── utils.py
│
├── scripts/
│   ├── simulate_esp32.py
│   ├── measure_latency.py
│   └── test_tts_queue.py
│
├── systemd/
│   └── visionx.service
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── ALERT_LOGIC.md
│   └── TEST_PLAN.md
│
├── logs/
├── metrics/
└── README.md
</pre>


--------------------------------------------------------------------------------
HOW IT WORKS
--------------------------------------------------------------------------------

1. ESP32 continuously measures distance using ultrasonic sensors and optionally GPS.
2. Sensor data is streamed as newline-terminated JSON over USB serial.
3. VisionX ingests sensor data asynchronously (non-blocking).
4. Camera frames are processed using YOLO (every N frames for performance).
5. Alert logic applies confidence thresholds and debounce rules.
6. Alerts are sent to a prioritized TTS queue.
7. Spoken feedback is delivered via Bluetooth earbuds.
8. Events are logged as structured JSON for later analysis.

--------------------------------------------------------------------------------
RUNNING WITHOUT HARDWARE (DEV MODE)
--------------------------------------------------------------------------------

Command:

python3 scripts/simulate_esp32.py | python3 -m visionx.visionx_main --mock-serial

Notes:
- Detection auto-disables if YOLO files are missing
- Full alert, TTS, and logging pipeline remains active

Logs are written to:

~/visionx_out/events.jsonl

--------------------------------------------------------------------------------
RASPBERRY PI DEPLOYMENT (SUMMARY)
--------------------------------------------------------------------------------

1. Install dependencies: OpenCV, Picamera2, espeak-ng
2. Place YOLO files in ~/models/
3. Pair Bluetooth earbuds
4. Enable systemd service:

sudo cp systemd/visionx.service /etc/systemd/system/
sudo systemctl enable visionx
sudo systemctl start visionx

--------------------------------------------------------------------------------
WHY THIS PROJECT MATTERS
--------------------------------------------------------------------------------

VisionX is not a demo script. It is an engineered system designed around:

- Hardware variability
- Limited compute
- Non-blocking I/O
- Fault tolerance
- Deployment and maintenance

This project demonstrates applied skills in:

- Embedded systems
- Edge AI
- Concurrent programming
- Software architecture
- Production-quality Python

--------------------------------------------------------------------------------
FUTURE IMPROVEMENTS
--------------------------------------------------------------------------------

- Directional alerts (left/right depth)
- Dynamic distance-based speech modulation
- Model quantization for faster inference
- Field testing with quantitative metrics

--------------------------------------------------------------------------------
AUTHOR
--------------------------------------------------------------------------------

Shivam Thanki  
Computer Science | Embedded Systems | Edge AI  

GitHub: https://github.com/shivamthanki-coder
