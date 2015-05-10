import beads.*;
import org.jaudiolibs.beads.*;
import ddf.minim.*;

 import processing.serial.*;
 
 Serial myPort;        // The serial port
 
 //Defines for the different states of the wheel
 final char OFF = 'o';
 final char WINNER = 'w';
 final char SPIN = 's';
 final char LOSE = 'l';
 
 //Globals for our sound objects and players
  AudioPlayer offSong;
  AudioPlayer winSong;
  AudioPlayer spinSong;
  AudioPlayer loseSong;
  Minim minim;

 
 char state = OFF;
 
 void setup () {
   // set the window size:
   size(400, 300);        
   
   // List all the available serial ports
   println(Serial.list());
   // Seems like com 4 is com11, which is what i'm using
   myPort = new Serial(this, Serial.list()[4], 9600);
   // don't generate a serialEvent() unless you get a newline character:
   //myPort.bufferUntil('\n');
   
   //Init all sound
   minim = new Minim(this);
   offSong = minim.loadFile("drunk.mp3", 2048);
   winSong = minim.loadFile("alarm.mp3", 2048);
   spinSong = minim.loadFile("spin.wav", 2048);
   loseSong = minim.loadFile("drunk.mp3", 2048);
   offSong.play();
   
   background(0);
 }
 void draw () {
   
   //Action based on states
   switch(state)
   {
      case WINNER: win();
                  break;
         
     case SPIN: spin();
                break;
      
   }
 }
 
 void spin()
 {
   offSong.pause();
   spinSong.play();
   //SPIN DA FRICKEN MOTORS, YA
   //Thread.sleep(spinSong.length());
 }
 
 void win()
 {
     println("WINNER!"); 
     offSong.pause();
     spinSong.pause();
     winSong.loop(3);
     winSong.play();
     int duration = winSong.length() * 4;
     int time = millis();
     while(millis() - time <= duration)
     {
         
     }
     //Thread.sleep(duration);
 }
 
 //read states from the arduino
 void serialEvent (Serial myPort) {
 // get the ASCII string:
 char inChar = myPort.readChar();
 
 if(inChar == OFF || inChar == WINNER || inChar == SPIN || inChar == LOSE)
{
    if (inChar != state) {
     // trim off any whitespace:
     //inString = trim(inString);
     state = inChar;
     println("We received " + inChar + " and our state is now " + state);
   }  
}
else //ignore anything that isn't one of our states
{
   //nothing to do
}
}
