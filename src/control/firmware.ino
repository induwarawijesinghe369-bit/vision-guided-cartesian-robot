
Paste:

```cpp
/*
 * Vision-Guided Cartesian Robot — Arduino firmware
 * Receives ASCII commands from Raspberry Pi over serial and drives
 * 3 stepper motors via A4988 drivers.
 *
 * Commands:
 *   HOME
 *   GOTO X<mm> Y<mm> Z<mm>
 *   PICK
 *   PLACE X<mm> Y<mm>
 *   JOG <axis><+|-><mm>
 *   STOP
 */

#include <AccelStepper.h>

// ---- Pin mapping (edit to match your build) ----
#define X_STEP 2
#define X_DIR  5
#define Y_STEP 3
#define Y_DIR  6
#define Z_STEP 4
#define Z_DIR  7
#define ENABLE 8

// ---- Mechanical constants ----
const float STEPS_PER_MM_X = 80.0;   // adjust
const float STEPS_PER_MM_Y = 80.0;
const float STEPS_PER_MM_Z = 400.0;

// ---- Soft limits (mm) ----
const float X_MIN = 0,   X_MAX = 300;
const float Y_MIN = 0,   Y_MAX = 300;
const float Z_MIN = 0,   Z_MAX = 80;

AccelStepper stepperX(AccelStepper::DRIVER, X_STEP, X_DIR);
AccelStepper stepperY(AccelStepper::DRIVER, Y_STEP, Y_DIR);
AccelStepper stepperZ(AccelStepper::DRIVER, Z_STEP, Z_DIR);

String inputLine = "";

void setup() {
  Serial.begin(115200);
  pinMode(ENABLE, OUTPUT);
  digitalWrite(ENABLE, LOW); // A4988 enable is active LOW

  stepperX.setMaxSpeed(1000);
  stepperX.setAcceleration(500);
  stepperY.setMaxSpeed(1000);
  stepperY.setAcceleration(500);
  stepperZ.setMaxSpeed(500);
  stepperZ.setAcceleration(250);

  Serial.println("OK READY");
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      handleCommand(inputLine);
      inputLine = "";
    } else {
      inputLine += c;
    }
  }
  stepperX.run();
  stepperY.run();
  stepperZ.run();
}

void handleCommand(String cmd) {
  cmd.trim();
  if (cmd.length() == 0) return;

  if (cmd == "HOME") {
    // TODO: run homing sequence using limit switches
    stepperX.setCurrentPosition(0);
    stepperY.setCurrentPosition(0);
    stepperZ.setCurrentPosition(0);
    Serial.println("OK DONE");
  }
  else if (cmd.startsWith("GOTO")) {
    // parse "GOTO X120 Y80 Z5"
    float x = extractAxis(cmd, 'X');
    float y = extractAxis(cmd, 'Y');
    float z = extractAxis(cmd, 'Z');
    if (!inLimits(x, y, z)) { Serial.println("ERR 02"); return; }
    stepperX.moveTo(x * STEPS_PER_MM_X);
    stepperY.moveTo(y * STEPS_PER_MM_Y);
    stepperZ.moveTo(z * STEPS_PER_MM_Z);
    Serial.println("OK");
  }
  else if (cmd == "STOP") {
    stepperX.stop();
    stepperY.stop();
    stepperZ.stop();
    Serial.println("OK");
  }
  else {
    Serial.println("ERR 01");
  }
}

float extractAxis(String cmd, char axis) {
  int idx = cmd.indexOf(axis);
  if (idx < 0) return 0;
  int end = cmd.indexOf(' ', idx);
  String val = (end < 0) ? cmd.substring(idx + 1) : cmd.substring(idx + 1, end);
  return val.toFloat();
}

bool inLimits(float x, float y, float z) {
  return x >= X_MIN && x <= X_MAX &&
         y >= Y_MIN && y <= Y_MAX &&
         z >= Z_MIN && z <= Z_MAX;
}
