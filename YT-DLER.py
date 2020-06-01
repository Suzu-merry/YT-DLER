print('Please wait...')
import os
import random
import re
import string
from pytube import Playlist
from pytube import YouTube
import PySimpleGUI as sg

def sanitize(filename):
    return filename.translate(str.maketrans('', '', string.punctuation))
    
def make_ordinal(n):
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix
    
def dlVideo(videoURL,audioOnly,outputFolder = None):
    video = YouTube(videoURL)
    videoTitle = sanitize(video.title)
    if audioOnly:
        video.streams.filter(subtype='mp4', only_audio=True).first().download(filename=videoTitle, output_path=outputFolder)
    else:
        video.streams.get_highest_resolution().download(filename=videoTitle, output_path=outputFolder)
    return videoTitle
    
def processURL(target,audioOnly):
    if 'playlist?' in target:
        playlist = Playlist(target)
        playlistName = sanitize(playlist.title())
        print(f'Playlist: {playlistName}')
        if not os.path.isdir(playlistName):
            os.mkdir(playlistName)
            print(f'Created folder for playlist: {playlistName}')
        playlist_length = len(playlist.video_urls)
        print("Videos in playlist:", playlist_length)
        count = 0
        failure_count = 0
        while True:
            try:
                if count in range(playlist_length):
                    videoURL = playlist.video_urls[count]
                    result = dlVideo(videoURL,audioOnly,playlistName)
                    print(f'Successfully downloaded {result}, {make_ordinal(count+1)} video from {playlistName}')
                    count+=1
                else:
                    break
            except:
                try:
                    print(f'Failed to download {make_ordinal(count+1)} video from{playlistName}, retrying...')
                    result = dlVideo(videoURL,audioOnly,playlistName)
                    print(f'Successfully downloaded {result}, {make_ordinal(count+1)} video from {playlistName}')
                    count+=1
                except:
                    print(f'Failed to download {make_ordinal(count+1)} video from {playlistName}')
                    count+=1
                    failure_count+=1
                    pass
        print("Successful:", count-failure_count)
        print("Failed:", failure_count)
    else:
        try:
            result = dlVideo(target,audioOnly)
            print(f'Successfully downloaded {result}')
        except:
            try:
                print(f'Failed to download video\nretrying...')
                result = dlVideo(target,audioOnly)
                print(f'Successfully downloaded {result}')
                count+=1
            except:
                print(f'Failed to download video')
                count+=1
                failure_count+=1
                pass
        
sg.theme('Black')	
main_label = sg.Text('Welcome to the YT-DLer')
sub_label = sg.Text('Enter a YT URL:')
input_text_box = sg.InputText()
audio_button = sg.CBox('Audio only')
download_button = sg.Button('Download')
cancel_button = sg.Button('Cancel')

layout = [  [main_label],
            [sub_label, input_text_box],
            [audio_button, download_button, cancel_button] ]

window = sg.Window('YT-DLer 1.0', layout)
print('YT-DLer 1.0','https://github.com/Suzu-merry/YT-DLER','Ready...',sep='\n')
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    print('Beginning download...')
    textInput = values[0]
    audioOnly = values[1]
    if 'youtube.com' in textInput or 'youtu.be' in textInput:
        processURL(textInput,audioOnly)
    print('Ready for a new link!')
window.close()
print('boop!')