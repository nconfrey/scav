import processing.serial.*;
import processing.sound.*;

Serial myPort;  // Create object from Serial class
String val;     // Data received from the serial port
int score = 0;

//sound effect go here:
SoundFile test;

void setup() {
  fullScreen();
  
  //setup serial
  try
  {
    String portName = Serial.list()[0]; //change the 0 to a 1 or 2 etc. to match your port
    myPort = new Serial(this, portName, 9600);
  }
  catch(Exception e)
  {
    print("FUCK there is no serial");
  }
    
  
  //setup screen visuals
  textSize(32);
  text("SCORE: " + score, 10, 30); 
  fill(0, 102, 153);
  
  //set up speaker output
  test = new SoundFile(this, "sample.mp3");
}

void parse(String sensorData)
{
   switch(sensorData)
   {
      case "1": 
        score += 10;
        break;
      case "2": 
        score += 10;
        break;
      case "3": 
        score += 50;
        break;
      case "4": 
        score += 50;
        break;
   }
}

void draw() {
  if ( myPort.available() > 0) 
  {  // If data is available,
    val = myPort.readStringUntil('\n');         // read it and store it in val
  }
  if(val == null)
    return;
  parse(val);
}