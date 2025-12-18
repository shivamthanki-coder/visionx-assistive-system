# VisionX — Wearable Assistive Vision System

VisionX is a modular, real-time assistive system designed to help visually impaired users perceive nearby obstacles using computer vision, proximity sensing, and audio feedback.

The system combines **YOLO-based object detection**, **ultrasonic distance sensing**, and a **prioritized text-to-speech (TTS) pipeline**, engineered to run headlessly on a Raspberry Pi with an ESP32 acting as a sensor reflex unit.

---

## Key Features

- **Real-time object detection** using YOLOv3-tiny (optimized for edge devices)
- **Sensor fusion**: camera vision + ultrasonic distance + optional GPS
- **Non-blocking, prioritized TTS queue** with deduplication
- **Hardware-mockable pipeline** for development without physical devices
- **Cross-platform development** (macOS/Linux) with Raspberry Pi deployment
- **Structured logging** for evaluation, debugging, and metrics
- **Systemd-ready** for auto-start on boot

---

## System Architecture (High Level)

ESP32 (Ultrasonic + GPS)
│
│ JSON over Serial (USB)
▼
Raspberry Pi (VisionX Core)
├─ Picamera2 → YOLO Detection
├─ Alert Logic + Debounce
├─ Priority TTS Queue
└─ Structured Event Logging
│
▼
Bluetooth Earbuds (Audio Feedback)

---

## Repository Structure

visionx-assistive-system/
├── visionx/
├── scripts/
├── systemd/
├── docs/
├── logs/
├── metrics/
└── README.md

---

## Running Without Hardware (Recommended for Dev)

```bash
python3 scripts/simulate_esp32.py | python3 -m visionx.visionx_main --mock-serial
Logs are written to:
~/visionx_out/events.jsonl
Raspberry Pi Deployment (Summary)
sudo cp systemd/visionx.service /etc/systemd/system/
sudo systemctl enable visionx
sudo systemctl start visionx
Author
Shivam Thanki
Computer Science | Embedded Systems | Edge AI
GitHub: https://github.com/shivamthanki-coder
