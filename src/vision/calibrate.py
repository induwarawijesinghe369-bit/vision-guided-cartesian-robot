"""
Homography calibration for the vision-guided Cartesian robot.

Click on N reference points in the camera preview whose millimetre
coordinates on the base plate are known. The script computes the
3x3 homography that maps pixel -> mm and saves it to config.yaml.

Usage:
    python calibrate.py

Controls:
    Left click  - record a point (in the same order as REFERENCE_MM below)
    r           - reset
    s           - save homography to config.yaml
    q / ESC     - quit
"""

import yaml
import cv2
import numpy as np

# --- Edit these to match your setup ---
# Known mm coordinates of the reference points on the base plate,
# in the SAME ORDER you will click them in the preview.
REFERENCE_MM = [
    (0,   0),
    (300, 0),
    (300, 300),
    (0,   300),
]

CAMERA_INDEX = 0
CONFIG_PATH = "config.yaml"

clicked_px = []

def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_px) < len(REFERENCE_MM):
        clicked_px.append((x, y))
        print(f"[click] pixel ({x}, {y}) -> mm {REFERENCE_MM[len(clicked_px)-1]}")

def save_homography(H):
    try:
        with open(CONFIG_PATH, "r") as f:
            cfg = yaml.safe_load(f) or {}
    except FileNotFoundError:
        cfg = {}
    cfg["homography"] = H.tolist()
    with open(CONFIG_PATH, "w") as f:
        yaml.safe_dump(cfg, f)
    print(f"[saved] homography written to {CONFIG_PATH}")

def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("[error] cannot open camera")
        return

    win = "calibrate — click each reference point in order"
    cv2.namedWindow(win)
    cv2.setMouseCallback(win, on_mouse)

    print(f"[info] click {len(REFERENCE_MM)} points in the preview, then press 's'.")

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        for i, (px, py) in enumerate(clicked_px):
            cv2.circle(frame, (px, py), 6, (0, 255, 0), -1)
            cv2.putText(frame, f"{i}: {REFERENCE_MM[i]}", (px + 8, py - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        cv2.putText(frame, f"{len(clicked_px)}/{len(REFERENCE_MM)} points",
                    (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

        cv2.imshow(win, frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or key == 27:
            break
        elif key == ord("r"):
            clicked_px.clear()
            print("[reset]")
        elif key == ord("s"):
            if len(clicked_px) != len(REFERENCE_MM):
                print(f"[warn] need {len(REFERENCE_MM)} points, have {len(clicked_px)}")
                continue
            src = np.array(clicked_px, dtype=np.float32)
            dst = np.array(REFERENCE_MM, dtype=np.float32)
            H, _ = cv2.findHomography(src, dst, method=0)
            if H is None:
                print("[error] homography failed — check point order")
                continue
            save_homography(H)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
