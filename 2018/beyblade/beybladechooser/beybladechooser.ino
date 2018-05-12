//www.elegoo.com
//2016.12.08
#include <Servo.h>
#include "IRremote.h"

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int closed = 5;    // variable to store the servo position
int openned=90;
int receiver = 11; // Signal Pin of IR receiver to Arduino Digital Pin 11

/*-----( Declare objects )-----*/
IRrecv irrecv(receiver);     // create instance of 'irrecv'
decode_results results;      // create instance of 'decode_results'

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);
  Serial.println("IR Receiver Button Decode"); 
  irrecv.enableIRIn(); // Start the receiver
}

void loop() 
{
  if (irrecv.decode(&results)) // have we received an IR signal?
  {
    Serial.println("got an ir");
    irrecv.resume(); // receive the next value
    myservo.write(openned);
    delay(100); 
    myservo.write(closed);
  }  
}

