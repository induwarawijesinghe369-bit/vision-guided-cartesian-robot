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

## Model

The vision system uses a custom-trained **YOLOv8** model to detect and classify 9 target objects on the workspace.

### Classes (9 total)

| Shape | Colors |
|---|---|
| Square  | red, green, blue |
| Circle  | red, green, blue |
| Hexagon | red, green, blue |

The color distinction is the harder part of the task — red, green and blue objects of the same shape share almost identical geometry, so classification depends on color cues that vary with lighting. Care was taken to control illumination over the workspace to keep classification stable.

### Training

- Base model: `yolov8n` (nano) — chosen for real-time inference on the Raspberry Pi
- Dataset: custom images captured with the same camera and lighting setup used at runtime, with the 9 classes labelled
- Data augmentation: standard Ultralytics augmentations (mosaic, HSV jitter, flips)
- Result: reliable detection of all 9 classes under the controlled workspace lighting

### Weights

The trained `.pt` weights are **not stored in this repository's git history** (to keep the repo small). When available, they will be attached as a GitHub Release — see the main README's **Model download** link.

To reproduce or extend this model:
1. Capture images of your own target objects with the same camera and lighting.
2. Label them (Roboflow, LabelImg, or CVAT).
3. Train: `yolo detect train data=dataset.yaml model=yolov8n.pt epochs=100 imgsz=640`
4. Drop `best.pt` into `models/` and set `model_path` in `config.yaml`.

## Setup

```bash
pip install ultralytics opencv-python pyserial numpy


