"""
YOLOv3-tiny detection wrapper.

If YOLO files are missing (common on dev machines),
the module falls back to a no-op detector so the rest
of the system can be tested.
"""

from pathlib import Path
import cv2
import numpy as np

from .config import (
    YOLO_CFG, YOLO_WEIGHTS, YOLO_NAMES,
    CAMERA_SIZE, CONF_THR, NMS_THR
)

# -------- Check model availability --------
_yolo_ready = True
for p in (YOLO_CFG, YOLO_WEIGHTS, YOLO_NAMES):
    if not Path(p).exists():
        _yolo_ready = False
        break

if not _yolo_ready:
    print("[detection] YOLO files not found — running in mock mode")

# -------- Load YOLO only if available --------
LABELS = []
net = None
ln = None

if _yolo_ready:
    with open(YOLO_NAMES, "r") as f:
        LABELS = [l.strip() for l in f if l.strip()]

    net = cv2.dnn.readNetFromDarknet(YOLO_CFG, YOLO_WEIGHTS)
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers().flatten()]


def detect(frame):
    """
    Run YOLO detection on a frame.
    Returns list of {label, conf, box}.
    In mock mode, always returns [].
    """
    if not _yolo_ready:
        return []

    (H, W) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(
        frame, 1 / 255.0, CAMERA_SIZE, swapRB=True, crop=False
    )
    net.setInput(blob)
    outputs = net.forward(ln)

    boxes, confidences, classIDs = [], [], []

    for out in outputs:
        for det in out:
            scores = det[5:]
            cid = int(np.argmax(scores))
            conf = float(scores[cid])
            if conf >= CONF_THR:
                box = det[0:4] * np.array([W, H, W, H])
                (cx, cy, w, h) = box.astype("int")
                x = int(cx - w / 2)
                y = int(cy - h / 2)
                boxes.append([x, y, int(w), int(h)])
                confidences.append(conf)
                classIDs.append(cid)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONF_THR, NMS_THR)

    results = []
    if len(idxs) > 0:
        for i in idxs.flatten():
            results.append({
                "label": LABELS[classIDs[i]],
                "conf": confidences[i],
                "box": boxes[i]
            })

    return results
