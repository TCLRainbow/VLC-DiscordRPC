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
print("Media: " + file)
mplayer.play()
file_name = file.split('/')[-1]
extension = file_name.split('.')[-1]
time.sleep(0.5)
length = mplayer.get_length() / 1000
media = mplayer.get_media()
mediaTrack_pp = ctypes.POINTER(vlc.MediaTrack)()
n = vlc.libvlc_media_tracks_get(media, ctypes.byref(mediaTrack_pp))
info = ctypes.cast(mediaTrack_pp, ctypes.POINTER(ctypes.POINTER(vlc.MediaTrack) * n))
media_track = info.contents[0].contents
audio = ctypes.cast(media_track.u.audio, ctypes.POINTER(vlc.AudioTrack))
sample = audio.contents.rate

details = f"{int(media_track.bitrate / 1000)}kbps {sample}Hz"
if length > 0:
    while True:
        snap = time.time()
        RPC.update(state=details, details=file_name, large_image=extension, party_id='xq', party_size=[1, 2**32],
                   large_text=extension, join='MTI4NzM0OjFpMmhuZToxMjMxMjM', start=int(snap), end=int(snap + length))
        time.sleep(length)
        mplayer.stop()
        mplayer.play()
else:
    while True:
        RPC.update(details=file_name, large_image=extension, large_text=extension, party_id='xq',
                   party_size=[1, 2**32], join='MTI4NzM0OjFpMmhuZToxMjMxMjM', start=int(time.time()))
        time.sleep(1)
        while mplayer.is_playing():
            time.sleep(0.5)
        mplayer.stop()
        mplayer.play()
