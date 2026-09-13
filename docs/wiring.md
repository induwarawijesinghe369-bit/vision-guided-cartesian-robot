# Wiring

## Raspberry Pi ↔ Arduino

- USB serial at 115200 baud.
- Pi acts as master, Arduino as slave.

## Arduino ↔ A4988 drivers

> Replace the pin numbers below with whatever you actually used.

| Signal | Arduino pin |
|---|---|
| X STEP | D2 |
| X DIR | D5 |
| Y STEP | D3 |
| Y DIR | D6 |
| Z STEP | D4 |
| Z DIR | D7 |
| ENABLE (shared) | D8 |

Each A4988 has:
- `STEP` → Arduino step pin
- `DIR` → Arduino dir pin
- `EN` → Arduino enable pin (shared)
- `MS1/MS2/MS3` → microstepping select (tie to GND or 5V)
- `VMOT` → 12V motor supply (with 100 µF electrolytic across VMOT/GND)
- `GND` → common ground
- `VDD` → 5V logic
- `1A 1B 2A 2B` → stepper coils

## Power

- 12 V 5 A PSU → A4988 `VMOT`
- 5 V from Arduino or a buck converter → A4988 `VDD`
- **Common ground** between Pi, Arduino and 12 V supply.

## Camera

- Pi Camera via CSI ribbon, or USB webcam via USB.
- Mounted rigidly above the workspace, looking straight down.
- Recommended: diffuse lighting to avoid shadows confusing YOLOv8.
