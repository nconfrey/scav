#!/usr/bin/env python

# Read lirc output, control video using the output

# Based on: https://github.com/akkana/scripts/blob/master/rpi/pyirw.py
#
## Read lirc output, in order to sense key presses on an IR remote.
## There are various Python packages that claim to do this but
## they tend to require elaborate setup and I couldn't get any to work.
## This approach requires a lircd.conf but does not require a lircrc.
## If irw works, then in theory, this should too.
## Based on irw.c, https://github.com/aldebaran/lirc/blob/master/tools/irw.c


import socket
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep

SOCKPATH = "/var/run/lirc/lircd"

sock = None

VIDEO_PATH = "./media/ocean_test.mp4"

def init_irw():
    global sock
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    print ('starting up irw on %s' % SOCKPATH)
    sock.connect(SOCKPATH)

def next_key():
    '''Get the next key pressed. Return keyname, updown.
    '''
    while True:
        data = sock.recv(128)
        # print("Data: " + data)
        data = data.strip()
        if data:
            break

    words = data.split()
    return words[2], words[1]

def run_player(player):
    while True:
        keyname, updown = next_key()
        print('%s (%s)' % (keyname, updown))
        if keyname == b'KEY_PLAY':
            if player.can_play():
                print('playing %s (%s)' % (keyname, updown))
                player.play()
            else:
                print('player cannot play %s (%s)' % (keyname, updown))
        elif keyname == b'KEY_PAUSE':
            if player.can_pause():
                player.pause()
                print('pausing %s (%s)' % (keyname, updown))
            else:
                print('player cannot pause %s (%s)' % (keyname, updown))
        elif keyname == b'KEY_POWER' and player:
            if player.can_quit():
                player.quit()
                print('quitting %s (%s)' % (keyname, updown))
                sleep(3)
                print('exiting program')
                break
            else:
                print('player cannot quit %s (%s)' % (keyname, updown))
        elif keyname == b'KEY_2':
            if player.can_seek():
                player.set_position(2)
                print('positioning to 2 %s (%s)' % (keyname, updown))
            else:
                print('player cannot seek %s (%s)' % (keyname, updown))
        elif keyname == b'KEY_4':
            if player.can_seek():
                player.set_position(4)
                print('positioning to 4 %s (%s)' % (keyname, updown))
            else:
                print('player cannot seek %s (%s)' % (keyname, updown))

    print('goodbye')


if __name__ == '__main__':

    init_irw()

    # Initialize the OMXPlayer and sleep to load in video
    player = OMXPlayer(VIDEO_PATH, args=['--no-osd'], pause=True)
    sleep(5)

    try:
        run_player(player)
    except Exception as e:
        player.quit()
        raise e
