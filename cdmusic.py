import glob
import os
import time

import vlc
from pypresence import Presence

song_name = input('Enter keyword for the song\n')
song_file = next(glob.iglob(f'{os.getenv("userprofile")}\\Music\\*{glob.escape(song_name)}*'))
mplayer = vlc.MediaPlayer(song_file, '-L')
print('Updating presence')
RPC = Presence('757258842328399944')
RPC.connect()
print(f"Now playing: {song_file}")


while True:
    mplayer.play()
    time.sleep(0.5)
    length = mplayer.get_length() / 1000
    print(length)
    snap = time.time()
    RPC.update(details=song_file.split('\\')[-1], start=int(snap), end=int(snap + length))
    time.sleep(length)
    mplayer.stop()
