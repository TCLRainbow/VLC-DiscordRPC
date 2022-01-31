import ctypes
import os
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import pytube
import vlc
from pypresence import Presence


def get_sample_rate(media):
    mediaTrack_pp = ctypes.POINTER(vlc.MediaTrack)()
    n = vlc.libvlc_media_tracks_get(media, ctypes.byref(mediaTrack_pp))
    info = ctypes.cast(mediaTrack_pp, ctypes.POINTER(ctypes.POINTER(vlc.MediaTrack) * n))
    media_track = info.contents[0].contents
    audio = ctypes.cast(media_track.audio, ctypes.POINTER(vlc.AudioTrack))  # Was media_track.u.audio in Sep 2020
    return audio.contents.rate

print('''
1. YouTube link
2. Local file
''')
x = int(input())

if x == 1:
    link = input('Paste YouTube link: ')
    extension = 'youtube'
    yt = pytube.YouTube(link)
    file_name = yt.title
    length = yt.length
    print('Downloading from YouTube')
    stream = yt.streams.get_audio_only('webm')
    file = stream.download(filename='cdmusic-youtube', skip_existing=False)
    mplayer = vlc.MediaPlayer(file)
    mplayer.play()
    time.sleep(2)
    sample = get_sample_rate(mplayer.get_media())
    details = f'{stream.abr} {sample}Hz'
else:
    Tk().withdraw()
    file = askopenfilename(initialdir=os.getenv("userprofile") + '\\Music')
    file_name = file.split('/')[-1]
    extension = file_name.split('.')[-1]
    mplayer = vlc.MediaPlayer(file)
    mplayer.play()
    time.sleep(3)

    length = mplayer.get_length() / 1000
    media = mplayer.get_media()
    sample = get_sample_rate(media)

    # Because media_track.bitrate is broken, Here is a replacement
    # In fact, this replacement allows bitrate to be calculated even for FLAC
    # But for files with bitrate, this method might be slightly inaccurate
    stats = vlc.MediaStats()
    vlc.libvlc_media_get_stats(media, stats)
    bitrate = int(stats.input_bitrate * 8000)

    details = f"~{bitrate}kbps {sample}Hz"


print('Updating presence')
RPC = Presence('757258842328399944')
RPC.connect()
print("Media: " + file)

if length > 0:
    while True:
        snap = time.time()
        RPC.update(state=details, details=file_name, large_image=extension, large_text=extension,
                   start=int(snap), end=int(snap + length))
        time.sleep(length)
        mplayer.stop()
        mplayer.play()
else:
    while True:
        RPC.update(state=details, details=file_name, large_image=extension, large_text=extension,
                   start=int(time.time()))
        while mplayer.is_playing():
            time.sleep(0.5)
        mplayer.stop()
        mplayer.play()
