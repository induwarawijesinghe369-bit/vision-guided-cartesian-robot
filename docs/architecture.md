# System Architecture

## Overview

The robot is organized into four layers:

1. **Perception** — camera + Raspberry Pi running YOLOv8 and OpenCV
2. **Planning** — pixel-to-robot coordinate transform and target selection
3. **Control** — Arduino + A4988 drivers + stepper motors
4. **Interface** — web UI for monitoring and manual jog

## Data flow
Camera frame
│
▼
Raspberry Pi

YOLOv8 inference

OpenCV filtering

Homography (pixel → mm)
│ serial @ 115200
▼
Arduino

Parse commands

Plan motion

Generate step/dir pulses


## Coordinate systems

| Frame | Unit | Notes |
|---|---|---|
| Camera | pixels (u, v) | Raw detection from YOLOv8 |
| Workspace | mm (x, y) | Base plate plane |
| Robot | steps | Motor pulses |

Transform pipeline:
1. **Pixel → mm** via homography calibrated from ≥4 reference points of known mm position on the base plate.
2. **mm → steps** using lead screw pitch and microstepping (e.g. 200 steps/rev × 16 microsteps / 2 mm pitch = 1600 steps/mm).

## Serial protocol

Raspberry Pi → Arduino (ASCII lines, `\n` terminated):

HOME
GOTO X120.5 Y80.0 Z5.0
PICK
PLACE X200 Y150
JOG X+10
STOP


Arduino → Pi:

OK
OK DONE
ERR 01 # unknown command
ERR 02 # soft-limit exceeded


## Safety

- Soft limits on all axes defined in firmware.
- `STOP` command halts motion immediately.
- Homing sequence on power-up before accepting motion commands.
- E-stop input on Arduino interrupt pin (planned).
│
▼
A4988 × 3 → NEMA 17 motors → End effector
