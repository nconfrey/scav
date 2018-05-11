# Item ???

> some description

## Requirements

Note: This should have requirements in a virtualenv but it's scav, so ain't nobody got time for that.

## Raspberry Pi

### Hardware & OS

We used a Raspberry Pi 3 for this project running Raspbian Stretch version 4.14 release date 2018-04-18. Downloaded from https://www.raspberrypi.org/downloads/raspbian/, but you may need to find this in an archive somewhere.

Install the OS, we flashed the microsd card using [Etcher](https://etcher.io/).

### Video Player

package: `python-omxplayer-wrapper`

```
# Prereqs
sudo apt-get update && sudo apt-get install -y libdbus-1{,-dev}

# Install the package
pip3 install omxplayer-wrapper
```

(Or follow the installation instructions here: http://python-omxplayer-wrapper.readthedocs.io/en/latest/)

Gotchas:

- The OMXPlayer wrapper can only have one video per instance as per https://github.com/willprice/python-omxplayer-wrapper/issues/73 thus we work around this by concatenating all of our videos together and simply seekingto play different snippets.

### IR Reciever Setup

- https://gist.github.com/prasanthj/c15a5298eb682bde34961c322c95378b
- http://shallowsky.com/blog/hardware/raspberry-pi-ir-remote.html
- http://alexba.in/blog/2013/01/06/setting-up-lirc-on-the-raspberrypi/
- https://www.raspberrypi.org/forums/viewtopic.php?t=192891

## Arduino

### Microcontrollers

- Arduino Uno rev3

### Parts List

- **6** Velleman ARDUINO® COMPATIBLE 1838 IR INFRARED 37.9 kHz RECEIVER - https://www.velleman.eu/products/view/?id=435548
- **MANY** female-female, male-female, male-male breadboard jumper wires - no link
- **1** Elagoo IR remote control - no link
