"""
Vision-guided Cartesian robot — main vision loop.

Captures frames from a camera, runs YOLOv8 inference, filters detections,
converts pixel centroids to workspace millimetres via a homography, and
sends motion commands to an Arduino over serial.

NOTE
----
The trained YOLOv8 weights are NOT included in this repository. Before
running, either:
  - Place your trained model at models/best.pt and update MODEL_PATH below, OR
  - Use a pretrained checkpoint (e.g. yolov8n.pt) and adjust CLASS_FILTER.

Configuration is read from config.yaml. See docs/architecture.md for the
pixel -> mm -> steps pipeline.
"""

import time
import yaml
import cv2
import numpy as np
import serial
from ultralytics import YOLO

# ---------- Config ----------
CONFIG_PATH = "config.yaml"

def load_config(path=CONFIG_PATH):
    defaults = {
        "camera_index": 0,
        "model_path": "models/best.pt",
        "confidence": 0.5,
        "class_filter": None,          # e.g. ["cube", "bolt"] or None for all
        "serial_port": "/dev/ttyUSB0",
        "baud": 115200,
        "workspace_mm": {"x": 300, "y": 300},
        "homography": None,            # 3x3 list, produced by calibrate.py
    }
    try:
        with open(path, "r") as f:
            user = yaml.safe_load(f) or {}
        defaults.update(user)
    except FileNotFoundError:
        print(f"[warn] {path} not found — using defaults")
    return defaults

# ---------- Homography ----------
def pixel_to_mm(px, py, H):
    """Apply 3x3 homography to a pixel point. Returns (x_mm, y_mm)."""
    pt = np.array([px, py, 1.0])
    mapped = H @ pt
    if mapped[2] == 0:
        return None
    return mapped[0] / mapped[2], mapped[1] / mapped[2]

# ---------- Serial ----------
class RobotLink:
    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud, timeout=1)
        time.sleep(2)  # let Arduino reset
        # drain startup banner
        while self.ser.in_waiting:
            print("[arduino]", self.ser.readline().decode(errors="ignore").strip())

    def send(self, cmd):
        print("[pi -> arduino]", cmd)
        self.ser.write((cmd + "\n").encode())
        reply = self.ser.readline().decode(errors="ignore").strip()
        print("[arduino]", reply)
        return reply

# ---------- Main loop ----------
def main():
    cfg = load_config()

    # Load model
    try:
        model = YOLO(cfg["model_path"])
    except Exception as e:
        print(f"[error] could not load model at {cfg['model_path']}: {e}")
        print("        see note at top of this file about retraining.")
        return

    # Load homography
    if cfg["homography"] is None:
        print("[error] no homography in config.yaml — run calibrate.py first")
        return
    H = np.array(cfg["homography"], dtype=np.float64)

    # Open camera
    cap = cv2.VideoCapture(cfg["camera_index"])
    if not cap.isOpened():
        print("[error] cannot open camera")
        return

    # Connect to Arduino
    try:
        link = RobotLink(cfg["serial_port"], cfg["baud"])
    except Exception as e:
        print(f"[error] serial connection failed: {e}")
        return

    link.send("HOME")

    print("[info] running — press q in the preview window to quit")
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            results = model(frame, conf=cfg["confidence"], verbose=False)
            detections = []

            for r in results:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    label = model.names[cls_id]
                    if cfg["class_filter"] and label not in cfg["class_filter"]:
                        continue
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                    mm = pixel_to_mm(cx, cy, H)
                    if mm is None:
                        continue
                    detections.append((label, cx, cy, mm))

                    # draw
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)),
                                  (0, 255, 0), 2)
                    cv2.putText(frame, f"{label} ({mm[0]:.0f},{mm[1]:.0f})mm",
                                (int(x1), int(y1) - 8),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            # Send the first detection as a demo pick
            if detections:
                label, _, _, (x_mm, y_mm) = detections[0]
                link.send(f"GOTO X{x_mm:.1f} Y{y_mm:.1f} Z0")
                link.send("PICK")

            cv2.imshow("vision", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        link.ser.close()

if __name__ == "__main__":
    main()
