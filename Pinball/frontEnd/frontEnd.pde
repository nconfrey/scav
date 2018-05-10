import processing.serial.*;
import processing.sound.*;

Serial myPort;  // Create object from Serial class
String val;     // Data received from the serial port
int score = 0;
int colorval = 0;
int highscore = 0;
int update = 1;
int multiball = 0;
int mostRecent = 0;

//sound effect go here:
SoundFile multiballSound;
SoundFile bumperHit;
SoundFile ambient;

void setup() {
  fullScreen();
  
  //setup serial
  String portName = Serial.list()[1]; //change the 0 to a 1 or 2 etc. to match your port
  myPort = new Serial(this, portName, 9600);
  
  //setup screen visuals
  background(36,39,250);
  textSize(32);
  textAlign(CENTER, CENTER);
  textSize(45);
  text("" + score, 900, 550);
  fill(0, 102, 153);
  
  //set up speaker output
  multiballSound = new SoundFile(this, "C:\\Users\\Nick Confrey\\Documents\\Projects\\scav\\Pinball\\frontEnd\\MULTIBALL.mp3");
  bumperHit = new SoundFile(this, "C:\\Users\\Nick Confrey\\Documents\\Projects\\scav\\Pinball\\frontEnd\\hit.mp3");
  ambient = new SoundFile(this, "C:\\Users\\Nick Confrey\\Documents\\Projects\\scav\\Pinball\\frontEnd\\ambient.mp3");
  ambient.play();
}

void parse(String sensorData)
{
  //println(Integer.parseInt(sensorData));
  int current =  Integer.parseInt(sensorData.charAt(0)+"");
  if(current == mostRecent) {
    return;
  } else {
    mostRecent = current;
  }
  
   switch(current)
   {
      case 3: 
        score += 10;
        bumperHit.play();
        break;
      case 2: 
        score += 10;
        bumperHit.play();
        break;
      case 4: 
        score += 50;
        bumperHit.play();
        break;
      case 1: 
        score += 50;
        multiball = 120;
        multiballSound.play();
        break;
      case 5:
        score = 0;
   }
}

void draw() {
  delay(10);
  colorval+= update;
  if(colorval == 255) {
     update = -1; 
  } else if(colorval == 0) {
    update = 1; 
  }
  
  background(colorval, 0, 255-colorval);
  color(0, 255-colorval, colorval);
  textAlign(CENTER, CENTER);
  textSize(200);
  text("" + score, 900, 550);
  fill(0, 102, 153);
  
  textAlign(LEFT,TOP);
  textSize(45);
  text("Highscore: " + highscore, 20, 20);
  fill(0, 102, 153);
  
  if(multiball > 0) {
    textAlign(CENTER,TOP);
    multiball--;
    textSize(120);
    text("Multiball!", 900, 250);
    text("Multiball!", 900, 750);
  }
  
  if ( myPort.available() > 0) 
  {  // If data is available,
    val = myPort.readStringUntil('\n');         // read it and store it in val
  }
  if(val == null)
    return;
  print(val);
  parse(val);
  if(score > highscore) {
    highscore = score;
    //Do something exciting
  }
}