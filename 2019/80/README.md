## Installation

1. Ensure you have Java 8 installed

`java -version`

2. Install the Java RXTX Library (serial)

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

## Implementation Plan

### Components

- [HSRMKeyboardHero Fork](https://github.com/nconfrey/HSRMKeyboardHero) Computer as main brain (Forked from [martinjuhasz](https://github.com/martinjuhasz), modifications by [Nick](https://github.com/nconfrey) & [Em](https://github.com/eurbs))
- [./touch_board](./touch_board) Serial port is opened to read from touch board ([Nick](https://github.com/nconfrey))
- [./el_sequencer](./el_sequencer) Serial port is opened to write to EL Sequencer ([Em](https://github.com/eurbs))
