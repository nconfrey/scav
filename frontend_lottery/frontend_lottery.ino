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

/* ======================== */

//Defines for the different states of the wheel
const char OFF    = 'o';
const char WINNER = 'w';
const char SPIN   = 's';
const char LOSE   = 'l';

char state     = OFF;
char old_state = OFF; //used to track changes of the state


/* PINS */
const int coin_input_pin = 1;
const int ledPin = 13;

/* Wheel init {pin, offset} */
wheel_t wheels[N_WHEELS] = {
    {2, 0, HIGH, 8, 10},
    {3, 0, HIGH, 9, 20},
    {4, 0, HIGH, 10, 30}
};

void setup(){
    // initialize the serial communication:
    Serial.begin(9600);

    /* initialize pins */
    pinMode(coin_input_pin, INPUT);
    pinMode(ledPin, OUTPUT);
    for (int i = 0; i < N_WHEELS; i++){
        pinMode(wheels[i].pin, INPUT);
        pinMode(wheels[i].brake_pin, OUTPUT);
    }
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
        } else if (voltage == LOW){
            wheels[i].voltage = LOW;
            //analogWrite(ledPin, 100);
        }
        if (wheels[i].offset >= wheels[i].brake_threshold){
           digitalWrite(wheels[i].brake_pin, HIGH);
        }
    }
}

void loop() {
    //digitalWrite(wheels[0].brake_pin, HIGH);
    update_wheel_offsets();
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
