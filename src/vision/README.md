# Vision Module

YOLOv8 + OpenCV pipeline running on the Raspberry Pi.

## Files (planned)

- `main.py` — capture loop, detection, coordinate transform, send to Arduino
- `calibrate.py` — homography calibration from reference points
- `config.yaml` — camera index, model path, workspace size

## Pipeline

1. Grab frame from camera.
2. Run YOLOv8 inference → bounding boxes + class labels.
3. Filter detections by class/confidence.
4. Compute centroid of each box in pixel space.
5. Convert to mm using the calibrated homography.
6. Sort targets (e.g. nearest first) and send `GOTO / PICK / PLACE` commands over serial.

## Setup

```bash
pip install ultralytics opencv-python pyserial numpy
