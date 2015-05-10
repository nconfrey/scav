 //Defines for the different states of the wheel
 const char OFF = 'o';
 const char WINNER = 'w';
 const char SPIN = 's';
 const char LOSE = 'l';
 char state = OFF; 
 char old_state = state; //used to track changes of the state
 
const int button1Pin = 2;  // pushbutton 1 pin
const int button2Pin = 3;  // pushbutton 2 pin
const int ledPin =  13;    // LED pin

int count = 0; //if this reaches 5 (arbitrary) you win!

void setup() {
  // initialize the serial communication:
  Serial.begin(9600);
  
  pinMode(button1Pin, INPUT);
  pinMode(button2Pin, INPUT);
  pinMode(ledPin, OUTPUT);
  
}

void loop() {
  int button1State, button2State;  // variables to hold the pushbutton states
  button1State = digitalRead(button1Pin);
  button2State = digitalRead(button2Pin);
  // So the state will be LOW when it is being pressed,
  // and HIGH when it is not being pressed.
  if(button2State == LOW)
    count++;
  if(count >= 10){
    state = WINNER;
    count = 0;
  }
  if(button1State == LOW)
    state = SPIN;
  // send the value of analog input 0:
  if(old_state != state)
  {
    Serial.println(state);
    old_state = state;
  }
  switch(state)
  {
     case WINNER: break;
     case SPIN: break;
  }
  // wait a bit for the analog-to-digital converter 
  // to stabilize after the last reading:
  delay(10);
}
