# Item 80

> Your team’s archaeologists uncovered an ancient civilization’s musical contraption, and using a technological interface of your own, you’ve brought it to life! Your rhythm game-style interface can use buttons, lights, circuitry, and any other wonders of our modern age to provide prompts and feedback for your 1 to 2 minute song, but the actual sounds should all be produced using physical parts of the contraption. Of course, just like in other rhythm games, missing prompts will cause some of your corresponding sounds not to play. [225 points] †

## Implementation

### Components

- [HSRMKeyboardHero Fork](https://github.com/nconfrey/HSRMKeyboardHero) Computer as main brain (Forked from [martinjuhasz](https://github.com/martinjuhasz), modifications by [Nick](https://github.com/nconfrey) & [Em](https://github.com/eurbs))
- [./touch_board](./touch_board) Serial port is opened to read from touch board ([Nick](https://github.com/nconfrey))

### Beat-Mapping

The song "Sandstorm" was beatmapped by Emilee by memorizing the song rhythm and "recording" the actions which needed to be performed.

## Quickstart

### Prerequisites

1. Clone this repo

2. Clone [HSRMKeyboardHero Fork](https://github.com/nconfrey/HSRMKeyboardHero)

3. Ensure you have Java 8 installed

`java -version`

4. Install the Java RXTX Library (serial)

Some resources:
- Comprehensive guide: https://cs.iupui.edu/~xiaozhon/course_tutorials/Arduino_and_Java_Serial.pdf
- For non-windows: https://playground.arduino.cc/Interfacing/Java/
- For 64 bit Mac OS X: http://blog.iharder.net/2009/08/18/rxtx-java-6-and-librxtxserial-jnilib-on-intel-mac-os-x/ (search "we have a librxtxSerial.jnilib file" and download the `librxtxSerial.jnilib` file)

Test to see if it's working by running:

```
scav/2019/80 $ cd SerialTest
scav/2019/80/SerialTest $ javac SerialTest
scav 2019/80/SerialTest $ java SerialTest
```

Your output should look like this:

```
Experimental:  JNI_OnLoad called.
Stable Library
=========================================
Native lib Version = RXTX-2.1-7
Java lib Version   = RXTX-2.1-7
Could not find COM port.
Started
```

5. Wire up a [Touch Board](https://www.bareconductive.com/shop/touch-board/) with 5 inputs (E0 through E4)

### Run

1. Use Eclipse to load [HSRMKeyboardHero Fork](https://github.com/nconfrey/HSRMKeyboardHero). Add your serial port.
2. Turn on the Touch Board and plug it into your computer
3. Start the HSMRKeyboardHero fork and ensure the serial port connection opens to the touch board
4. Play!


## Credits

- **Build**: Mike & Nick
- **Electronics**: Nick & Emilee
- **Paint**: Sydney & Everyone
- **Decoration**: Sydney, Maria, Geoffrey, Annie
- **Beat Mapping**: Emilee
- **Presentation**: Emilee & Nick

