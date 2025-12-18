from pathlib import Path

# ===== Serial (ESP32) =====
SER_PORTS = ["/dev/ttyUSB0", "/dev/ttyUSB1"]
SER_BAUD = 9600

# ===== Camera =====
CAMERA_SIZE = (320, 320)
FRAME_STRIDE = 2   # process every Nth frame

# ===== YOLO =====
YOLO_CFG = str(Path.home() / "models/yolov3-tiny.cfg")
YOLO_WEIGHTS = str(Path.home() / "models/yolov3-tiny.weights")
YOLO_NAMES = str(Path.home() / "models/coco.names")
CONF_THR = 0.35        # lower to 0.20 for demos
NMS_THR = 0.35

# ===== Alerts =====
PERSON_HITS_REQUIRED = 2
SAVE_INTERVAL_SEC = 3.0

# ===== TTS =====
TTS_RATE = 160
TTS_VOICE = "en"
TTS_DEDUPE_SEC = 5.0
TTS_QUEUE_MAX = 20

# ===== Paths (OS-agnostic) =====
OUT_DIR = Path.home() / "visionx_out"
LOG_FILE = OUT_DIR / "events.jsonl"

# Ensure output directory exists
OUT_DIR.mkdir(parents=True, exist_ok=True)
