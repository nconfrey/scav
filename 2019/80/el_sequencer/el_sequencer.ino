/* Sketch for item 80
 *
 * Based on serial data, this will use the EL Sequencer to
 * serve as the GUI for a rhythm game.
 */

void setup() {
  // The EL channels are on pins 2 through 9
  // Initialize the pins as outputs
  pinMode(2, OUTPUT);  // channel A
  pinMode(3, OUTPUT);  // channel B
  pinMode(4, OUTPUT);  // channel C
  pinMode(5, OUTPUT);  // channel D
  pinMode(6, OUTPUT);  // channel E
  pinMode(7, OUTPUT);  // channel F
  pinMode(8, OUTPUT);  // channel G
  pinMode(9, OUTPUT);  // channel H -- no EL plugged in

  pinMode(13, OUTPUT); // status LED ("LED_BUILTIN")
}

void loop()
{
  unsigned long waitTime = 5 * 1000;
//  twoAtATime(waitTime);
  int i;
  for (i=0; i+=5; i++) {
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
  }
}

void twoAtATime(unsigned long waitTime)
{
  int x;  // pin number

  for (x=2; x<8; x+=2)
  {
    digitalWrite(x, HIGH);
    digitalWrite(x+1, HIGH);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(waitTime);
    digitalWrite(x, LOW);
    digitalWrite(x+1, LOW);
    digitalWrite(LED_BUILTIN, LOW);
  }
}
