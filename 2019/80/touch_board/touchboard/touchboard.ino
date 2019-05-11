// touch includes
#include <MPR121.h>
#include <Wire.h>
#define MPR121_ADDR 0x5C
#define MPR121_INT 4

// touch behaviour definitions
#define firstPin 0
#define lastPin 11

void setup() {
  Serial.begin(57600);

  while (!Serial) ; {} //uncomment when using the serial monitor
  Serial.println("ready to play those phat tunes yeah");

  if (!MPR121.begin(MPR121_ADDR)) Serial.println("error setting up MPR121");
  MPR121.setInterruptPin(MPR121_INT);

  MPR121.setTouchThreshold(40);
  MPR121.setReleaseThreshold(20);
}

void loop() {
  readTouchInputs();
}


void readTouchInputs() {
  if (MPR121.touchStatusChanged()) {
    MPR121.updateTouchData();
    for (int i = 0; i < 12; i++) { // Check which electrodes were pressed
      if (MPR121.isNewTouch(i)) {
        //pin i was just touched
        Serial.print("pin ");
        Serial.print(i);
        Serial.println(" was just touched");
      } else {
        if (MPR121.isNewRelease(i)) {
          Serial.print("pin ");
          Serial.print(i);
          Serial.println(" is no longer being touched");
        }
      }
    }
  }
}
