#!/usr/bin/env python3

from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep

VIDEO_PATH_OPENING = Path("./assets/opening.mp4")
VIDEO_PATH_BATTLE = Path("./assets/battle-test.mp4")

player_opening = OMXPlayer(VIDEO_PATH_OPENING, args=['--no-osd'], pause=True)

#player_battle = OMXPlayer(VIDEO_PATH_BATTLE)
#player_battle.pause()

sleep(5)

player_opening.play()

sleep(3)

player_opening.stop()
player_opening.quit()
print("quit opening player")

#sleep(3)

#print("creating new player instance for the battle")

#player_battle = OMXPlayer(VIDEO_PATH_BATTLE)

#sleep(5)

#player_battle.stop()

#sleep(3)

#player_opening.quit()
#player_battle.quit()

