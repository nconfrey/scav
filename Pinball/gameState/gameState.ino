/*
 * Scav 2017
 * 
 * For lightbulb:
 * 
 * orange is top
 * red is bottom outlet
 * yellow is ground
 * green is 5v
 */

//Define Pins
const int topOutlet = 8;
const int bottomOutlet = 9;
const int bumper1Pin = 10;
const int bumper2Pin = 11;
const int bumper3Pin = 12;
const int bumper4Pin = 13;

//Define game state machine
#define PREGAME 0
#define PLAYGAME 0

void setup() {
  pinMode(bottomOutlet, OUTPUT);
  pinMode(topOutlet, OUTPUT);
  pinMode(bumper1Pin, INPUT);
  pinMode(bumper2Pin, INPUT);
  pinMode(bumper3Pin, INPUT);
  pinMode(bumper4Pin, INPUT);
}

//for testing
void flickLED()
{
  digitalWrite(LED_BUILTIN, HIGH);
  digitalWrite(topOutlet, HIGH);
  digitalWrite(bottomOutlet, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(topOutlet, LOW);
  digitalWrite(bottomOutlet, LOW);
}

void loop() {
  if(digitalRead(bumper1Pin)) //if the first bumper is hit
  {
    flickLED();
    Serial.println("1");
  }
  if(digitalRead(bumper2Pin)) //if the second bumper is hit
  {
    flickLED();
    Serial.println("2");
  }
  if(digitalRead(bumper3Pin)) //if the third bumper is hit
  {
    flickLED();
    Serial.println("3");
  }
  if(digitalRead(bumper4Pin)) //if the fourth bumper is hit
  {
    flickLED();
    Serial.println("4");
  }
  

}
