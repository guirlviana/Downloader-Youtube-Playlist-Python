from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytube import YouTube
import os
from pytube import Playlist
from threading import Thread

# /------------------------------------------/
#
# @gvianadev - Guilherme Viana 
# My site -> http://bit.ly/guilhermevianadev
#
# /------------------------------------------/

class PlaylistDownloader():
    def __init__(self, playlistPath, folderPath) -> None:
        self.pathPlaylist = playlistPath
        self.pathFolder = folderPath

    def extractURLS(self): # extract the individual url to download
        links = []
        links = Playlist(self.pathPlaylist)        
        return links

    def download(self, links): # download the playlist
        for link in links:
            # download video
            try:            
                yt = YouTube(link)

                # replace the special characters to space
                title = yt.title
                print(title)
                new_title = ''
                for letter in title:
                    if letter == '|':
                        title.replace('|', ' ')
                    
                    elif letter == '>':
                        title.replace('>', ' ')
                    
                    elif letter == '<':
                        title.replace('<', ' ')
                    
                    elif letter == '?':
                        title.replace('?', ' ')
                    
                    elif letter == '*':
                        title.replace('*', ' ')
                    
                    elif letter == ':':
                        title.replace(':', ' ')
                    
                    elif letter == '/':
                        title.replace('/', ' ')
                    
                    elif letter == '\\':
                        title.replace('\\', ' ')
                    else:
                        new_title += letter

                yt.streams.filter(only_audio=True).first().download(self.pathFolder,filename=new_title)

            except Exception:
                print("It's not possible download video")
            
            else:
                print('Video downloaded succesfully')
            
    def convert(self, listFiles): # convert mp4 file to mp3
      
        for file in listFiles:
            
            root, ext = os.path.splitext(file)
            if ext == '.mp4':
                mp4_path = os.path.join(self.pathFolder, file)
                mp3_path = os.path.join(self.pathFolder, root + '.mp3')
                new_file = AudioFileClip(mp4_path)
                new_file.write_audiofile(mp3_path)
                os.remove(mp4_path)

    def divideList(self, list, length): # divide the downloads in 2 lists to open 2 threads
        new_list_to_convert = [[], []]
        
        if length / 2 == 0:
            half = int(length / 2)
            first_part = list[:half].copy()
            second_part = list[half:].copy()
            
            new_list_to_convert.insert(0, first_part)
            new_list_to_convert.insert(1, second_part)
            
        else:
            half = int(length / 2) + 1
            first_part = list[:half].copy()
            second_part = list[half:].copy()
            new_list_to_convert.insert(0, first_part)
            new_list_to_convert.insert(1, second_part)
        
        return new_list_to_convert

    def getMp4Infolder(self): # get the mp4 files in folder to convert
        cont = 0
        names = []
        for file in os.listdir(self.pathFolder):
            ext = os.path.splitext(file)[1]
            if ext == '.mp4':
                cont += 1
                names.append(file)
        return (cont, names)

   
 
def main(): # here the code that will execute
                                        # put your playlist link here 
    instance = PlaylistDownloader(  playlistPath = '',
                                    folderPath = r'')
                                        # put here the folder where your playlist will be downloaded
    
    # extract and format to download
    playlist_links = instance.extractURLS()                                
    playlist_links = instance.divideList(playlist_links, len(playlist_links))

    # download
    downloader1 = Thread(target=instance.download, daemon=True, args=[playlist_links[0]])
    downloader2 = Thread(target=instance.download, daemon=True, args=[playlist_links[1]])
    
    downloader1.start()
    downloader2.start()
    
    # close threads
    downloader1.join()
    downloader2.join()
    
    
    # extract and format to convert
    lengthMP4, list_of_songs = instance.getMp4Infolder()
    convert_list = instance.divideList(list_of_songs, lengthMP4)

    #convert
    converter1 = Thread(target=instance.convert, daemon=True, args=[convert_list[0]])
    converter2 = Thread(target=instance.convert, daemon=True, args=[convert_list[1]])
    
    converter1.start()
    converter2.start()
    
    # close threads
    converter1.join()
    converter2.join()
    
    print('All Done :)')

if __name__ == '__main__':
    main() # run application