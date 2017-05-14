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
const int buttonPin = 9;
const int topOutlet = 10;
const int bottomOutlet = 11;
const int bumper1Pin = 2;
const int bumper2Pin = 4;
const int bumper3Pin = 7;
const int bumper4Pin = 8;

//Define game state machine
#define PREGAME 0
#define PLAYGAME 1
int STATE = PREGAME;

void setup() {
  pinMode(bottomOutlet, OUTPUT);
  pinMode(topOutlet, OUTPUT);
  pinMode(bumper1Pin, INPUT);
  pinMode(bumper2Pin, INPUT);
  pinMode(bumper3Pin, INPUT);
  pinMode(bumper4Pin, INPUT);

  Serial.begin(9600);
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

void preGameLoop()
{
  if(digitalRead(buttonPin))
    STATE = PLAYGAME;
}

void playGameLoop()
{
  if(digitalRead(bumper1Pin) == HIGH) //if the first bumper is hit
  {
    //flickLED();
    Serial.println("1");
  }
  if(digitalRead(bumper2Pin) == HIGH) //if the second bumper is hit
  {
    //flickLED();
    Serial.println("2");
  }
  if(digitalRead(bumper3Pin) == HIGH) //if the third bumper is hit
  {
    //flickLED();
    Serial.println("3");
  }
  if(digitalRead(bumper4Pin) == HIGH) //if the fourth bumper is hit
  {
    //flickLED();
    Serial.println("4");
  }
}

void loop() 
{
  playGameLoop();
  delay(10);
}
