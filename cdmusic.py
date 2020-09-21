import ctypes
import os
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import vlc
from pypresence import Presence

Tk().withdraw()
file = askopenfilename(initialdir=os.getenv("userprofile") + '\\Music')
mplayer = vlc.MediaPlayer(file)
print('Updating presence')
RPC = Presence('757258842328399944')
RPC.connect()
print("Now playing: " + file)
mplayer.play()
file_name = file.split('/')[-1]
extension = file_name.split('.')[-1]
time.sleep(0.5)
length = mplayer.get_length() / 1000
media = mplayer.get_media()
mediaTrack_pp = ctypes.POINTER(vlc.MediaTrack)()
n = vlc.libvlc_media_tracks_get(media, ctypes.byref(mediaTrack_pp))
info = ctypes.cast(mediaTrack_pp, ctypes.POINTER(ctypes.POINTER(vlc.MediaTrack) * n))
track = info.contents[0].contents
print(track)

details = f"{int(track.bitrate / 1000)}kbps"
if length > 0:
    while True:
        snap = time.time()
        RPC.update(state=details, details=file_name, large_image=extension, start=int(snap), end=int(snap + length))
        time.sleep(length)
        mplayer.stop()
        mplayer.play()
else:
    while True:
        RPC.update(state=details, large_image=extension, start=int(time.time()))
        while mplayer.is_playing():
            time.sleep(0.5)
        mplayer.stop()
        mplayer.play()
