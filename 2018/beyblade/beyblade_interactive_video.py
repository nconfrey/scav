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
VIDEO_VOLUME = -602
VIDEO_AUDIO_SOURCE = 'hdmi' # change to 'hdmi' to play audio over HDMI rather than headphone jack ('local')

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
        :param video_to_play_at_end
        """
        self.name = name
        self.startTime = startTime
        self.endTime = endTime
        self.nextVids = nextVids
        self.prevVid = prevVid
        # Default set to self -- the video will loop at the end. Else, will play the video specified (use set_end_vid).
        self._video_to_play_at_end = self

    def set_next_vids(self, next_vids):
        self.nextVids = next_vids

    def set_end_vid(self, video_to_play_at_end):
        """
        Use this method to override the default looping behavior by pointing to another video.
        :params video_to_play_at_end VidNode: Video that will play once the end time has been reached.
        """
        self._video_to_play_at_end = video_to_play_at_end

    def get_end_vid(self):
        return self._video_to_play_at_end

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
        self.in_crowd_mode = False
        # The following should be done in an iterator - used for handle_key_in_crowd_mode
        self.excited_idx = 0
        self.neutral_idx = 0
        self.negative_idx = 0
        # These are set in the tree creator - used for handle_key_in_crowd_mode
        cheer1_screen = VidNode(
            name='CHEER1_SCREEN',
            startTime=569,
            endTime=572,
        )
        cheer2_screen = VidNode(
            name='CHEER2_SCREEN',
            startTime=572,
            endTime=576,
        )
        boo1_screen = VidNode(
            name='BOO1_SCREEN',
            startTime=587,
            endTime=591,
        )
        boo2_screen = VidNode(
            name='BOO2_SCREEN',
            startTime=594,
            endTime=598,
        )
        nut1_screen = VidNode(
            name='NUT1_SCREEN',
            startTime=543,
            endTime=550,
        )
        nut2_screen = VidNode(
            name='NUT2_SCREEN',
            startTime=550,
            endTime=553,
        )

        self.excited_vids = [cheer1_screen, cheer2_screen]
        self.neutral_vids = [boo1_screen, boo2_screen]
        self.negative_vids = [nut1_screen, nut2_screen]

    def handle_key_in_crowd_mode(self, keyname):
        if keyname == b'KEY_1':
            idx = (self.excited_idx + 1) % len(self.excited_vids)
            self.currVid = self.excited_vids[idx]
            self.currVid.start_vid(self.player)
            self.excited_idx = idx
        elif keyname == b'KEY_2':
            idx = (self.negative_idx + 1) % len(self.negative_vids)
            self.currVid = self.negative_vids[idx]
            self.currVid.start_vid(self.player)
            self.negative_idx = idx
        elif keyname == b'KEY_3':
            idx = (self.neutral_idx + 1) % len(self.neutral_vids)
            self.currVid = self.neutral_vids[idx]
            self.currVid.start_vid(self.player)
            self.neutral_idx = idx

    def handle_key(self, keyname):
        print("Handling %s keypress for video %s" % (keyname, self.currVid.name))
        print(self.currVid.nextVids)
        # Global button handlers
        if keyname == b'KEY_BACK':
            self.currVid = self.vidTreeRoot
            self.currVid.start_vid(self.player)
            return
        elif keyname == b'KEY_9':
            self.currVid = VidNode(
                name='VICTORY_DRAW_SCREEN',
                startTime=605,
                endTime=620,
            )
            self.in_crowd_mode = False
            self.currVid.start_vid(self.player)
            return
        elif keyname == b'KEY_FORWARD' or keyname == b'KEY_FASTFORWARD':
            print('fast forwarding to end vid %s' % self.currVid.get_end_vid().name)
            self.currVid = self.currVid.get_end_vid()
            self.currVid.start_vid(self.player)
            return
        
        if self.in_crowd_mode:
            self.handle_key_in_crowd_mode(keyname)
            return

        # Handle move to next video
        if self.currVid.nextVids and isinstance(self.currVid.nextVids, list):
            for vid in self.currVid.nextVids:
                if keyname in vid.acceptedButtons:
                    print("Changing videos: %s -> %s", (self.currVid.name, vid.vidNode.name))
                    self.currVid = vid.vidNode
                    self.player.set_position(self.currVid.startTime)
                    # Dirty hack, needs more robust handling based on modes
                    if self.currVid.name == 'NUT1_SCREEN':
                        self.in_crowd_mode = True
                    return
        print("No action to take")

    def proceed(self):
        """Check to see if the video position is at or beyond the current video's end time.
        If so, set the current vid to the end vid and start playing at the end vid.
        """
        position_int = int(round(self.player.position()))
        if position_int == self.currVid.endTime:
            self.currVid = self.currVid.get_end_vid()
            self.currVid.start_vid(self.player)



# =======================
#        MAIN CODE
# =======================

def create_beyblade_vid_tree():

    # Define tree nodes

    title_screen = VidNode(
        name='TITLE_SCREEN',
        startTime=376,
        endTime=408,
    )
    character_select_screen = VidNode(
        name='CHARACTER_SELECT_SCREEN',
        startTime=409,
        endTime=423,
    )
    no_fight_credits_screen = VidNode(
        name='NO_FIGHT_CREDITS_SCREEN',
        startTime=665,
        endTime=677,
    )
    restart_screen = VidNode(
        name='RESTART_SCREEN',
        startTime=678,
        endTime=713,
    )
    true_ending_screen = VidNode(
        name='TRUE_ENDING_SCREEN',
        startTime=714,
        endTime=777,
    )
    congrats_screen = VidNode(
        name='CONGRATS_SCREEN',
        startTime=651,
        endTime=664,
    )
    cheer1_screen = VidNode(
        name='CHEER1_SCREEN',
        startTime=569,
        endTime=572,
    )
    cheer2_screen = VidNode(
        name='CHEER2_SCREEN',
        startTime=572,
        endTime=576,
    )
    boo1_screen = VidNode(
        name='BOO1_SCREEN',
        startTime=587,
        endTime=591,
    )
    boo2_screen = VidNode(
        name='BOO2_SCREEN',
        startTime=594,
        endTime=598,
    )
    nut1_screen = VidNode(
        name='NUT1_SCREEN',
        startTime=543,
        endTime=548,
    )
    nut2_screen = VidNode(
        name='NUT2_SCREEN',
        startTime=550,
        endTime=553,
    )
    all_character_selected_screen = VidNode(
        name='CHAR_SELECTED_SCREEN',
        startTime=528,
        endTime=543,
    )
    victory_draw_screen = VidNode(
        name='VICTORY_DRAW_SCREEN',
        startTime=605,
        endTime=620,
    )
    choose1_gold_black_screen = VidNode(
        name='CHOOSE1_GB_SCREEN',
        startTime=498,
        endTime=513,
    )
    choose1_kh_screen = VidNode(
        name='CHOOSE1_KH_SCREEN',
        startTime=427,
        endTime=438,
    )
    choose1_red_green_screen = VidNode(
        name='CHOOSE1_RG_SCREEN',
        startTime=483,
        endTime=498,
    )
    choose2_kh_gb_screen = VidNode(
        name='CHOOSE2_KH_GB_SCREEN',
        startTime=453,
        endTime=468,
    )
    choose2_rg_gb_screen = VidNode(
        name='CHOOSE2_RG_GB_SCREEN',
        startTime=513,
        endTime=528,
    )
    choose2_kh_rg_screen = VidNode(
        name='CHOOSE2_KH_GB_SCREEN',
        startTime=438,
        endTime=453,
    )
    # Link nodes
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
            acceptedButtons=[bytes('KEY_{}'.format(i + 1), encoding='utf-8'),
            b'KEY_CHANNELUP', b'KEY_CHANNELDOWN'],
            vidNode=selectable_intro_vids[i],
        ))
    intro_vid.set_next_vids(intro_next_vids)

    for index in range(len(selectable_intro_vids)):
        vid = selectable_intro_vids[index]
        vid.set_end_vid(title_screen)
        vid.set_next_vids([
            NextVid(
                acceptedButtons=[b'KEY_CHANNELUP', b'KEY_CHANNELDOWN'],
                vidNode=selectable_intro_vids[(index + 1) % 5],
            ),
        ])

    title_screen.set_next_vids([
        NextVid(
            acceptedButtons=[b'KEY_GREEN'],
            vidNode=character_select_screen,
        ),
        NextVid(
            acceptedButtons=[b'KEY_RED'],
            vidNode=no_fight_credits_screen
        ),
    ])

    no_fight_credits_screen.set_end_vid(restart_screen);

    restart_screen.set_next_vids([
        NextVid(
            acceptedButtons=[b'KEY_GREEN'],
            vidNode=title_screen
        ),
        NextVid(
            acceptedButtons=[b'KEY_RED'],
            vidNode=true_ending_screen
        ),
    ])

    character_select_screen.set_next_vids([
        NextVid(
            acceptedButtons=[b'KEY_1'],
            vidNode=choose1_gold_black_screen
        ),
        NextVid(
            acceptedButtons=[b'KEY_2'],
            vidNode=choose1_kh_screen
        ),
        NextVid(
            acceptedButtons=[b'KEY_3'],
            vidNode=choose1_red_green_screen
        ),
    ])

    choose1_gold_black_screen.set_next_vids([
        NextVid(
            acceptedButtons=[b'KEY_2'],
            vidNode=choose2_kh_gb_screen
        ),
        NextVid(
            acceptedButtons=[b'KEY_3'],
            vidNode=choose2_rg_gb_screen
        )
    ])

    choose1_kh_screen.set_next_vids([
        NextVid(
            acceptedButtons=[b'KEY_1'],
            vidNode=choose2_kh_gb_screen
        ),
        NextVid(
            acceptedButtons=[b'KEY_3'],
            vidNode=choose2_kh_rg_screen
        )
    ])

    choose1_red_green_screen.set_next_vids([
        NextVid(
            acceptedButtons=[b'KEY_1'],
            vidNode=choose2_kh_rg_screen
        ),
        NextVid(
            acceptedButtons=[b'KEY_2'],
            vidNode=choose2_rg_gb_screen
        )
    ])

    choose2_rg_gb_screen.set_end_vid(nut1_screen)
    choose2_kh_rg_screen.set_end_vid(nut1_screen)
    choose2_kh_gb_screen.set_end_vid(nut1_screen)

    victory_draw_screen.set_end_vid(congrats_screen)
    congrats_screen.set_end_vid(true_ending_screen)
    true_ending_screen.set_end_vid(restart_screen)

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
    sock.settimeout(0.05)
    print ('starting up irw on %s' % SOCKPATH)
    sock.connect(SOCKPATH)

def next_key():
    '''Get the next key pressed. Return keyname, updown.

    Note: this is based on code we grabbed from github that I don't have a moment to
          completely understand right now. In any case, DO NOT try to exit the program
          with ctl-c. ctl-c will NOT kill the video while within the next_key loop.
          Instead, use the power button to exit gracefully as programmed.
    '''
    data = b''
    try:
        data = sock.recv(128)
    except socket.timeout:
        return None, None
    data = data.strip()
    if not data:
        return None, None

    words = data.split()
    return words[2], words[1]

def run_player(player_obj):
    player = player_obj.player

    while True:
        # Check to see if the video has ended
        # Dirty hack because I don't know a good way to have the object do this automatically
        player_obj.proceed()

        # Get keys and handle
        #print('Getting next key')
        keyname, updown = next_key()
        #print('%s (%s)' % (keyname, updown))
        if not keyname or updown != b'00':
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
        player_obj.player.quit()
        raise e

