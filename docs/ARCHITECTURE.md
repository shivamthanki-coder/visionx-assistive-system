# Architecture
- ESP32 -> serial JSON (ultrasonic + GPS)
- Raspberry Pi -> Picamera2 + YOLOv3-tiny
- TTS -> espeak-ng -> aplay -> Bluetooth earbuds
- Orchestrator fuses detections + sensors and enqueues TTS alerts
