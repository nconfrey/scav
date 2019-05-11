// Demo sketch for Sparkfun EL Sequencer
// Various example patterns
// Future: sync patterns to detected song's bpm


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
  
  pinMode(13, OUTPUT); // status LED
}

void loop() 
{
  float bpm = 20;
  unsigned long waitTime = getWaitTime(bpm);
  
  line(waitTime);
  zigzag(waitTime);
  twoAtATime(waitTime);
  fourAtATime(waitTime);
  upAndDown(waitTime);
  wave(waitTime);
}

/* Other Helper Functions */
void flashEL(int pin, unsigned long waitTime)
{
  digitalWrite(pin, HIGH);  // turn on EL channel
  delay(waitTime);
  digitalWrite(pin, LOW);   // turn off EL channel
}

/* BPM Analysis Funcitons */

// Get the wait time from bpm
unsigned long getWaitTime(float bpm)
{
  // note: temporary function. currently uses a makeshift equation
  return bpm;
}

/* Pattern Functions */
void line(unsigned long waitTime)
{
  int x,status;
  
  // Step through all eight EL channels (pins 2 through 9)
  for (x=2; x<=9; x++)
  {
    flashEL(x, waitTime);

    digitalWrite(13, status);     // bink status LED
    status = !status;
  }
}


void zigzag(unsigned long waitTime)
{
  int x; // pin number
  
  // Step through all eight EL channels forward then backward
  // Spend double time on each end channel
  for (x=2; x<=9; x++)
  {
    flashEL(x, waitTime);
  }
  for (x=9; x>=2; x--)
  {
    flashEL(x, waitTime);
  }
}

void twoAtATime(unsigned long waitTime)
{
  int x;  // pin number

  for (x=2; x<8; x+=2)
  {
    digitalWrite(x, HIGH);
    digitalWrite(x+1, HIGH);
    delay(waitTime);
    digitalWrite(x, LOW);
    digitalWrite(x+1, LOW);
  }
}

void fourAtATime(unsigned long waitTime)
{
  int x;  // pin number

  for (x=2; x<=9; x+=4)
  {
    digitalWrite(x, HIGH);
    digitalWrite(x+1, HIGH);
    digitalWrite(x+2, HIGH);
    digitalWrite(x+3, HIGH);
    delay(waitTime);
    digitalWrite(x, LOW);
    digitalWrite(x+1, LOW);
    digitalWrite(x+2, LOW);
    digitalWrite(x+3, LOW);
  }
}

void wave(unsigned long waitTime)
{
  // turn each on one by one, then back down
  // i think this is the wave
  int x;
  for (x=2; x<=9; x++)
  {
    digitalWrite(x, HIGH);
    delay(waitTime);
  }
  for (x=2; x<=9; x++)
  {
    digitalWrite(x, LOW);
    delay(waitTime);
  }
}

void upAndDown(unsigned long waitTime)
{
  // turn each on one by one, then back down
  // or is this the wave?
  int x;
  for (x=2; x<=9; x++)
  {
    digitalWrite(x, HIGH);
    delay(waitTime);
  }
  for (x=9; x>=2; x--)
  {
    digitalWrite(x, LOW);
    delay(waitTime);
  }
  delay(waitTime);
}
