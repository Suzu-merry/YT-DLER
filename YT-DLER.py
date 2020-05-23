print('Please wait...')
import os
import random
import re
import string
from pytube import Playlist
from pytube import YouTube
import PySimpleGUI as sg

def yt_url_dl(videoURL,audioOnly,outputFolder = None):
    try:
        video = YouTube(videoURL)
        if audioOnly:
            video.streams.filter(subtype='mp4', only_audio=True).first().download(filename=clean_filename(video.title), output_path=outputFolder)
        else:
            video.streams.get_highest_resolution().download(filename=clean_filename(video.title), output_path=outputFolder)
        print(f'Successfully downloaded {video.title}')
    except:
        try:
            print(f'Failed to download {video.title}... retrying...')
            if audioOnly:
                video.streams.filter(subtype='mp4', only_audio=True).first().download(filename=clean_filename(video.title), output_path=outputFolder)
            else:
                video.streams.get_highest_resolution().download(filename=clean_filename(video.title), output_path=outputFolder)
            print(f'Successfully downloaded {video.title}')
        except:
            print(f'Failed to download {video.title}')
            pass
    
def clean_filename(filename):
    return filename.translate(str.maketrans('', '', string.punctuation))
    
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
print('YT-DLer 1.0','fkn0wned.org','Ready...',sep='\n')
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    print('Beginning download...')
    textInput = values[0]
    audioOnly = values[1]
    if 'youtube.com' in textInput or 'youtu.be' in textInput:
        if 'playlist?' in textInput:
            playlist = Playlist(textInput)
            playlistName = playlist.title().translate(str.maketrans('', '', string.punctuation))
            print(f'Playlist: {playlistName}')
            if not os.path.isdir(playlistName):
                os.mkdir(playlistName)
                print(f'Created folder for playlist: {playlistName}')
            count = 0
            print("Videos in playlist:", len(playlist.video_urls))
            while True:
                try:
                    playlist_length = len(playlist.video_urls)
                    if count in range(playlist_length):
                        videoURL = playlist.video_urls[count]
                        yt_url_dl(videoURL,audioOnly,playlistName)
                        count+=1
                    else:
                        break
                except:
                    pass
            count = 0
        else:
            yt_url_dl(textInput,audioOnly)
    print('Ready for a new link!')
window.close()
print('boop!')
