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

import os
import socket
import subprocess
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep

# =======================
#      IR RECEIVER
# =======================
SOCKPATH = "/var/run/lirc/lircd"

sock = None


# =======================
#    VIDEO SETTINGS
# =======================
VIDEO_PATH = "./media/beyblade-semi-interactable-v1.mp4"
# note: -602 is about 50% volume and -2000 is 10% volume. todo: add source
VIDEO_VOLUME = -3000
VIDEO_AUDIO_SOURCE = 'local' # change to 'hdmi' to play audio over HDMI rather than headphone jack

# =======================
#  AUDIO ACCENT SETTINGS
# =======================
AUDIO_CHEER_PATH = os.path.join(os.getcwd(), 'media', 'small_crowd_cheer.wav')

# =======================
#  VIDEO TREE STRUCTURE
# =======================

class VidNode(object):
    def __init__(self, startTime, endTime, nextVids=[], prevVid=None):
        """
        :param startTime int: start time in seconds
        :param endTime int: end time of video in seconds
        :param nextVids list(NextVid):
        :param prevVid VidNode:
        """
        self.startTime = startTime
        self.endTime = endTime
        self.nextVids = nextVids
        self.prevVid = prevVid

class NextVid(object):
    def __init__(self, acceptedButtons, vidNode):
        """
        :param acceptedButtons list(byte str): list of IR buttons that can be used to transition to this video from the previous video
        :param vidNode VidNode: the actual pointer to the next video:
        """
        self.acceptedButtons = acceptedButtons
        self.vidNode = vidNode

class VidPlayer(object):
    """Wrapper around the omxplayer containing positions in the interactive video
    (composition pattern)
    """
    def __init__(self, player, vidTreeRoot):
        self.player = player
        self.vidTreeRoot = vidTreeRoot
        self.currVid = vidTreeRoot



# =======================
#        MAIN CODE
# =======================

def init_player():
    return None

def init_irw():
    global sock
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    print ('starting up irw on %s' % SOCKPATH)
    sock.connect(SOCKPATH)

def next_key():
    '''Get the next key pressed. Return keyname, updown.

    Note: this is based on code we grabbed from github that I don't have a moment to
          completely understand right now. In any case, DO NOT try to exit the program
          with ctl-c. ctl-c will NOT kill the video while within the next_key loop.
          Instead, use the power button to exit gracefully as programmed.
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
        if updown != b'00':
            # Only take the first signal. Ignore if person is pressing and holding button.
            continue
        # TODO: move default play/pause & power keys to video player object
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
        elif keyname == b'KEY_POWER':
            if player and player.can_quit():
                player.quit()
                print('quitting %s (%s)' % (keyname, updown))
                sleep(1)
            break

    print('goodbye')


if __name__ == '__main__':

    init_irw()

    # Initialize the OMXPlayer and sleep to load in video
    prod_args = ['--no-osd', '--vol', str(VIDEO_VOLUME), '-o', VIDEO_AUDIO_SOURCE]
    dev_args = ['--win', '0,40,600,400', '--no-osd', '--vol', str(VIDEO_VOLUME), '-o', VIDEO_AUDIO_SOURCE]
    player = OMXPlayer(VIDEO_PATH, dev_args, pause=True)
    player.pause()
    sleep(3)

    try:
        run_player(player)
    except Exception as e:
        player.quit()
        raise e

