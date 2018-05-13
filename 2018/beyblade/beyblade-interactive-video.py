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

# TODO: get/set functions for classes
# TODO: use pythonic snake case as opposed to camelCase (oops)

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
    def __init__(self, name, startTime, endTime, nextVids=[], prevVid=None):
        """
        :param name str: name of the video for identification, SCREAMING_CASE
        :param startTime int: start time in seconds
        :param endTime int: end time of video in seconds
        :param nextVids list(NextVid): List of nextvids. Make sure there are no overlaps of accepted buttons for nextVids.
        :param prevVid VidNode:
        """
        self.name = name
        self.startTime = startTime
        self.endTime = endTime
        self.nextVids = nextVids
        self.prevVid = prevVid

    def set_next_vids(self, next_vids):
        self.nextVids = next_vids

    def start_vid(self, player):
        player.set_position(self.startTime)

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

    def handle_key(self, keyname):
        print("Handling %s keypress for video %s" % (keyname, self.currVid.name))
        print(self.currVid.nextVids)
        # Global button handlers
        if keyname == b'KEY_BACK':
            self.currVid = self.vidTreeRoot
            self.currVid.start_vid(self.player)

        # Handle move to next video
        if self.currVid.nextVids and isinstance(self.currVid.nextVids, list):
            for vid in self.currVid.nextVids:
                if keyname in vid.acceptedButtons:
                    print("Changing videos: %s -> %s", (self.currVid.name, vid.vidNode.name))
                    self.currVid = vid.vidNode
                    self.player.set_position(self.currVid.startTime)
                    return
        print("No action to take")


# =======================
#        MAIN CODE
# =======================

def create_beyblade_vid_tree():
    intro_vid = VidNode(name='INTRO',
                       startTime=0,
                       endTime=78)
    selectable_intro_vids = [
        VidNode(
            name='J_INTRO',
            startTime=79,
            endTime=168,
        ),
        VidNode(
            name='BE_INTRO',
            startTime=169,
            endTime=210,
        ),
        VidNode(
            name='ME_INTRO',
            startTime=211,
            endTime=255,
        ),
        VidNode(
            name='POKE_INTRO',
            startTime=256,
            endTime=315,
        ),
        VidNode(
            name='OS_INTRO',
            startTime=316,
            endTime=375,
        ),
    ]
    intro_next_vids = []
    for i in range(len(selectable_intro_vids)):
        intro_next_vids.append(NextVid(
            acceptedButtons=[bytes('KEY_{}'.format(i + 1), encoding='utf-8')],
            vidNode=selectable_intro_vids[i],
        ))
    intro_vid.set_next_vids(intro_next_vids)
    return intro_vid

def init_player_obj():
    # Initialize the OMXPlayer and sleep to load in video
    prod_args = ['--no-osd', '--vol', str(VIDEO_VOLUME), '-o', VIDEO_AUDIO_SOURCE]
    dev_args = ['--win', '0,40,600,400', '--no-osd', '--vol', str(VIDEO_VOLUME), '-o', VIDEO_AUDIO_SOURCE]
    player = OMXPlayer(VIDEO_PATH, dev_args, pause=True)
    player.pause()
    sleep(5)
    vid_tree_root = create_beyblade_vid_tree()
    player_obj = VidPlayer(player, vid_tree_root)
    print("Player ready")
    return player_obj

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

def run_player(player_obj):
    player = player_obj.player

    while True:
        print('Getting next key')
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
        else:
            player_obj.handle_key(keyname)

    print('goodbye')


if __name__ == '__main__':

    init_irw()
    player_obj = init_player_obj()

    try:
        run_player(player_obj)
    except Exception as e:
        player.quit()
        raise e

