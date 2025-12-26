# VisionX — Wearable Assistive Vision System

**One-line:** Edge-ready wearable that fuses camera + ultrasonic sensing to issue prioritized spoken alerts to visually impaired users.

**Why it matters:** The system combines YOLO-based object detection, ultrasonic distance sensing, and a prioritized text-to-speech (TTS) pipeline, engineered to run headlessly on a Raspberry Pi with an ESP32 acting as a sensor reflex unit.

## RUNNING WITHOUT HARDWARE (DEV MODE)

### Quickstart (dev – no hardware)

Follow these exact commands to run a simulated demo in a fresh environment.

```bash
# clone repository
git clone https://github.com/shivamthanki-coder/visionx-assistive-system.git
cd visionx-assistive-system

# create & activate virtualenv
python3 -m venv .venv
source .venv/bin/activate

# upgrade pip and install python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```
### Dev-mode: simulate ESP32 serial → pipe into VisionX main

Run the simulator (no hardware required):

```bash
python3 scripts/simulate_esp32.py | python3 -m visionx.visionx_main --mock-serial
```
### Output (sample)
```bash

Events are written to the output folder:
tail -n 5 ~/visionx_out/events.jsonl

``` 
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
RASBERRYPIE PI DEPLOYMENT (PRODUCTION)
--------------------------------------------------------------------------------

1. Install dependencies: OpenCV, Picamera2, espeak-ng
2. Place YOLO files in ~/models/
3. Pair Bluetooth earbuds
4. Enable systemd service:

```bash
# copy service file (adjust ExecStart path as needed)
sudo cp systemd/visionx.service /etc/systemd/system/visionx.service

# reload systemd and enable the service at boot
sudo systemctl daemon-reload
sudo systemctl enable visionx.service

# start service now and follow logs
sudo systemctl start visionx.service
sudo journalctl -u visionx.service -f
```

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
CONTRIBUTION
--------------------------------------------------------------------------------
## Contributors

- **Zalak Thakkar** — Sensor integration support, validation, and Code generation.
- **Darshan Tita** — Code logic generation, algorithm review, and implementation support
  
--------------------------------------------------------------------------------
AUTHOR
--------------------------------------------------------------------------------

Shivam Thanki  
ICT Engineer | Embedded Systems | Edge AI  

## LICENSE

MIT License

GitHub: https://github.com/shivamthanki-coder
