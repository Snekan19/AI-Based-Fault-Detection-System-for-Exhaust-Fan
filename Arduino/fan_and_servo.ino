#include <Servo.h>

Servo myServo;

// Pin connections
const int SERVO_PIN = 9;
const int FAN_PWM_PIN = 3;       // 4-pin fan PWM wire
const int FAN_POWER_PIN = 7;     // MOSFET gate pin
const int BUZZER_PIN = 8;        // Buzzer pin

// Servo angles
const int SERVO_NORMAL = 30;
const int SERVO_FULL_OPEN = 90;

// Fan PWM values
const int FAN_FULL_SPEED = 255;
const int FAN_STOP_SPEED = 0;

// Latch flags
bool fault2Latched = false;
bool fault3Latched = false;

// --- NEW: Global variables for non-blocking buzzer patterns ---
unsigned long previousBuzzerMillis = 0;
bool buzzerToneState = false;
int currentActiveFault = 0;
// --------------------------------------------------------------

void applyOutputs(int servoAngle, bool fanPower, int fanPWM, bool buzzerState) {
  // Servo control
  myServo.write(servoAngle);

  // Fan control
  if (fanPower) {
    digitalWrite(FAN_POWER_PIN, HIGH);   // MOSFET ON
    analogWrite(FAN_PWM_PIN, fanPWM);
  } else {
    analogWrite(FAN_PWM_PIN, FAN_STOP_SPEED);
    digitalWrite(FAN_POWER_PIN, LOW);    // MOSFET OFF, fan fully stops
  }

  // Buzzer control (REMOVED from here to allow pattern generation in the main loop)
  // digitalWrite(BUZZER_PIN, buzzerState ? HIGH : LOW);
}

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);

  myServo.attach(SERVO_PIN);

  pinMode(FAN_PWM_PIN, OUTPUT);
  pinMode(FAN_POWER_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  // Initial safe state before LabVIEW starts
  applyOutputs(SERVO_NORMAL, false, FAN_STOP_SPEED, false);
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    // Reset command from LabVIEW
    if (input == "R" || input == "RESET") {
      fault2Latched = false;
      fault3Latched = false;
      currentActiveFault = 0; // Reset buzzer pattern

      applyOutputs(SERVO_NORMAL, true, FAN_FULL_SPEED, false);

      Serial.println("System Reset: Fan ON, Servo Normal, Buzzer OFF");
      return;
    }

    int faultCode = input.toInt();
    if (faultCode == 1){
      fault2Latched = false;
    }

    // Latch fault 2
    if (faultCode == 2) {
      fault2Latched = true;
    }

    // Latch fault 3
    // Fault 3 has higher priority
    if (faultCode == 3) {
      fault3Latched = true;
    }

    int servoAngle = SERVO_NORMAL;
    int fanPWM = FAN_FULL_SPEED;
    bool fanPower = true;
    bool buzzerState = false;

    // Priority 1: Fault 3
    if (fault3Latched) {
      // Fault 3: fan stop forever until reset
      servoAngle = SERVO_FULL_OPEN;
      fanPower = false;
      fanPWM = FAN_STOP_SPEED;
      buzzerState = true;
      faultCode = 3;
    }

    // Priority 2: Fault 2
    else if (fault2Latched) {
      // Fault 2: fan runs continuously, servo full open
      servoAngle = SERVO_FULL_OPEN;
      fanPower = true;
      fanPWM = FAN_FULL_SPEED;
      buzzerState = true;
      faultCode = 2;
    }

    // Normal / other faults
    else {
      if (faultCode == 1) {
        // Normal operation
        servoAngle = SERVO_NORMAL;
        fanPower = true;
        fanPWM = FAN_FULL_SPEED;
        buzzerState = false;
      }
      else {
        // Invalid / unknown code
        servoAngle = SERVO_NORMAL;
        fanPower = false;
        fanPWM = FAN_STOP_SPEED;
        buzzerState = false;
      }
    }

    currentActiveFault = faultCode; // --- NEW: Update global fault state for the buzzer timer ---

    applyOutputs(servoAngle, fanPower, fanPWM, buzzerState);

    Serial.print("Fault Code: ");
    Serial.print(faultCode);
    Serial.print(" | Fault 2 Latched: ");
    Serial.print(fault2Latched ? "YES" : "NO");
    Serial.print(" | Fault 3 Latched: ");
    Serial.print(fault3Latched ? "YES" : "NO");
    Serial.print(" | Servo Angle: ");
    Serial.print(servoAngle);
    Serial.print(" | Fan Power: ");
    Serial.print(fanPower ? "ON" : "OFF");
    Serial.print(" | Fan PWM: ");
    Serial.print(fanPWM);
    Serial.print(" | Buzzer: ");
    Serial.println(buzzerState ? "ON (Pattern)" : "OFF");
  }

  // --- NEW: Non-blocking Buzzer Pattern Generator ---
  unsigned long currentMillis = millis();
  int buzzerInterval = 0;

  // Assign intervals based on the active latched fault
  if (currentActiveFault == 2) {
    buzzerInterval = 500; // Slow beep (500ms) for Fault 2
  } else if (currentActiveFault == 3) {
    buzzerInterval = 100; // Fast beep (100ms) for Fault 3 (Highest Priority)
  }

  // Execute pattern or turn off entirely
  if (buzzerInterval > 0) {
    if (currentMillis - previousBuzzerMillis >= buzzerInterval) {
      previousBuzzerMillis = currentMillis;
      buzzerToneState = !buzzerToneState; // Toggle state
      digitalWrite(BUZZER_PIN, buzzerToneState ? HIGH : LOW);
    }
  } else {
    digitalWrite(BUZZER_PIN, LOW); // Ensure it stays off during normal operation
    buzzerToneState = false;
  }
  // --------------------------------------------------
}