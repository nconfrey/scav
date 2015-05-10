/* ======== HEADER ======== */
#define N_WHEELS 3

typedef struct wheel {
    int pin;
    int offset;
    unsigned char voltage;
    int brake_pin;
    int brake_threshold;
} wheel_t;

void update_wheel_offsets();
void test_brake(int i);
void reset_wheels();
void transition_to_state(int _state);

/* ======================== */

//Defines for the different states of the wheel
const char OFF    = 'o';
const char WINNER = 'w';
const char SPIN   = 's';
const char SPUN   = 't';
const char LOSE   = 'l';

char state     = OFF;
char old_state = OFF; //used to track changes of the state


/* PINS */
const int coin_input_pin = 0;
const int ledPin = 13;

/* Wheel init {pin, offset} */
wheel_t wheels[N_WHEELS] = {
    {5, 0, HIGH, 8, 10},
    {6, 0, HIGH, 9, 15},
    {7, 0, HIGH, 10, 30}
};

void test_brake(int i)
{
    digitalWrite(wheels[i].brake_pin, HIGH);
    delay(50);
    digitalWrite(wheels[i].brake_pin, LOW);
}

void setup(){
    // initialize the serial communication:
    Serial.begin(9600);

    /* initialize pins */
    pinMode(coin_input_pin, INPUT);
    pinMode(ledPin, OUTPUT);
    for (int i = 0; i < N_WHEELS; i++){
        pinMode(wheels[i].pin, INPUT);
        pinMode(wheels[i].brake_pin, OUTPUT);
        test_brake(i);
    }
    state = SPIN;
}

void update_wheel_offsets()
{
    for (int i = 0; i < N_WHEELS; i++){
        int voltage = digitalRead(wheels[i].pin);
        if (voltage == HIGH && wheels[i].voltage == LOW){
            // we've gone from low to high voltage, this means that
            // the spoke has made contact again
            wheels[i].voltage = HIGH;
            wheels[i].offset++; 
            digitalWrite(ledPin, HIGH); 
        } if (voltage == LOW && wheels[i].voltage == HIGH){
            // we've gone from high to low voltage, this means that
            // the spoke left contact with slinky. do nothing.
        }
        if (voltage == LOW){
            wheels[i].voltage = LOW;
            digitalWrite(ledPin, LOW);            
        } else {
            digitalWrite(ledPin, HIGH);
        }
        if (wheels[i].offset >= wheels[i].brake_threshold){
           digitalWrite(wheels[i].brake_pin, HIGH);
        }
    }
    int all_above_threshold = 1;
    for (int i = 0; i < N_WHEELS; i++){
      if (wheels[i].offset < wheels[i].brake_threshold){
        all_above_threshold = 0;
        break;
      }
    }
    if (all_above_threshold){
      transition_to_state(SPUN);
    }
}

void reset_wheels()
{
    for (int i = 0; i < N_WHEELS; i++){
        digitalWrite(wheels[i].brake_pin, LOW);
    }
}

void transition_to_state(int _state)
{
    //Serial.println(_state);
    state = _state;
}

void loop() {

    if (state == OFF){
      transition_to_state(SPIN);
    } else if (state == SPIN){
      update_wheel_offsets();
    } else if (state == SPUN){
      delay(3000);
      reset_wheels();
      transition_to_state(SPIN);
    }  
    delay(10);
    
}

    // int coin_input_state = digitalRead(coin_input_pin);

    //if (button1State == LOW)
    //    state = SPIN;

    // send the value of analog input 0:
    //if (old_state != state){
    //   Serial.println(state);
    //   old_state = state;
    //}
    

    
    //switch (state){
    //  case WINNER: break;
    //  case SPIN: break;
    //}

    // wait a bit for the analog-to-digital converter
    // to stabilize after the last reading:
