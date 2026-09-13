# Vision-Guided Cartesian Pick-and-Place Robot

A Raspberry Pi-based Cartesian (gantry) robot that detects objects using computer vision, computes their position, and autonomously picks and places them using stepper-motor-driven axes.

---

## 📌 Overview

This project combines **mechanical design**, **computer vision**, **embedded motor control** and a **web-based interface** into a single automated pick-and-place system. A camera mounted above the workspace captures the scene; a YOLOv8 + OpenCV pipeline detects and localizes target objects; the coordinates are transformed into robot-space commands; and stepper motors drive the X, Y and Z axes to pick and place the object.

The goal was to build a complete mechatronic system — not just a vision demo or a motor demo — and to integrate all subsystems into a working robot.

---

## 🎯 Objectives

- Design and fabricate a rigid Cartesian (gantry) frame with three axes of motion.
- Implement real-time object detection and localization using YOLOv8 and OpenCV.
- Convert camera pixel coordinates into robot workspace coordinates.
- Drive three stepper motors precisely using A4988 drivers.
- Provide a simple web interface for monitoring and manual control.
- Integrate vision, motion control and the user interface into one system.

---

## 🧠 System Architecture

Camera → Raspberry Pi (YOLOv8 + OpenCV) → Arduino → A4988 drivers → Steppers → End effector

More detail will be added in `docs/architecture.md`.

---

## 🛠️ Hardware

| Component | Purpose |
|---|---|
| Raspberry Pi | Vision processing, high-level control |
| Arduino (Uno/Nano) | Real-time stepper control |
| A4988 stepper drivers × 3 | Drive X, Y, Z motors |
| NEMA 17 stepper motors × 3 | Axis motion |
| Pi Camera / USB camera | Object detection |
| 12V PSU | Motor power |
| Linear rails, belts, bearings | Mechanical motion |
| End effector (gripper) | Pick and place |

---

## 💻 Software

### Vision (`src/vision/`)
- YOLOv8 model for object detection
- OpenCV for frame capture, filtering and coordinate extraction
- Pixel → robot coordinate transform

### Control (`src/control/`)
- Arduino firmware for stepper motion
- Serial command protocol from Raspberry Pi → Arduino
- Homing, jogging and pick-place routines

### Communication (`src/communication/`)
- Serial link between Pi and Arduino
- Web interface for monitoring and manual control

---

## 🚀 Getting Started

Coming soon — instructions for running the vision pipeline and uploading the Arduino firmware.

---

## 📁 Repository Structure

vision-guided-cartesian-robot/
├── README.md
├── docs/ # architecture, wiring, BOM
├── src/
│ ├── vision/ # YOLOv8 + OpenCV pipeline
│ ├── control/ # Arduino firmware + motion
│ └── communication/
├── cad/ # SolidWorks / STEP files
└── images/ # photos, screenshots, diagrams


---

## 🗺️ Roadmap

- [x] Mechanical frame design and fabrication
- [x] Stepper motor control via A4988
- [x] YOLOv8 detection pipeline
- [x] Coordinate mapping pixel → robot space
- [x] Serial communication Pi ↔ Arduino
- [x] Web interface
- [ ] Full closed-loop pick-and-place demo
- [ ] Gripper upgrade
- [ ] Demo video

---

## 👤 Author

**Induwara Wijesinghe**  
Mechanical Engineering Undergraduate — Mechatronics  
University of Moratuwa  
📧 induwarawijesinghe369@gmail.com
