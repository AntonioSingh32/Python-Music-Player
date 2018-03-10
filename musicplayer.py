#musicplayer.py
#Antonio Singh
#Music Player programmed in Python that utilizes Mutagen, Pygame and Tkinter modules to allow user to select their personal directory for songs and play them

import os
import pygame

from tkinter.filedialog import askdirectory
from mutagen.id3 import ID3
#from mutagen.id3 import APIC
#from mutagen.mp3 import MP3
#from mutagen.id3 import PictureType
from tkinter import *

#from mutagen import File

root = Tk()
root.minsize(500,500)
scrollbar = Scrollbar(root, orient="vertical")

songs = []
names = []
artist = []
album = []
#arrays created to be filled later on using ID3 tags

index = 0

v = StringVar()
a = StringVar()
y = StringVar()
#p = PhotoImage()

songlabel = Label (root, textvariable = v, width = 35)
artistlabel = Label (root, textvariable = a, width = 35)
albumlabel = Label (root, textvariable = y, width = 35)

frmcur_text = StringVar()

#incremenets index so user can skip to next song and updates label at same time
def skipsong(event):

    global index
    index += 1
    pygame.mixer.music.load(songs[index])
    pygame.mixer.music.play()
    updatelabel()

#decrements index so user can rewingd to previous song and updates label at same time
def backsong(event):

    global index
    index -= 1
    pygame.mixer.music.load(songs[index])
    pygame.mixer.music.play()
    updatelabel()

def stopsong(event):

    pygame.mixer.music.stop()
    v.set("")
    a.set("")
    y.set("")

def playsong(event):

    pygame.mixer.music.play()
    updatelabel()

def updatelabel ():

    global index
    global songname

    v.set(names[index])
    a.set(artist[index])
    y.set(album[index])

#identifies what user selects in click event and uses information to identify index of selected song and play the song
def onselect(event):

    global index

    w = event.widget
    i = int(w.curselection()[0])

    frmcur_text.set(i)

    index = i

    pygame.mixer.music.load(songs[index])
    pygame.mixer.music.play()
    updatelabel()

#allows user to select their directory for music files
def directoryselector():

    directory = askdirectory()
    os.chdir(directory)

    for files in os.listdir(directory):

        if files.endswith(".mp3"):
        #searches users chosen directory and if any file with extension mp3 is found within it appens the file to songs array

            #realdir = os.path.realpath(files)
            #audio = ID3(realdir)
            #picture_type = PictureType.COVER_FRONT
            #frame = APIC(type=picture_type)

            songs.append(files)


            try:
                realdir = os.path.realpath(files)
                audio = ID3(realdir)

                names.append(audio['TIT2'].text[0])
                artist.append(audio['TPE1'].text[0])
                album.append(audio['TALB'].text[0])

            except:

                names.append(files)
                artist.append(files)



            print(files)

    pygame.mixer.init()
    pygame.mixer.music.load(songs[0])
    pygame.mixer.music.play()

directoryselector()

label = Label(root, text="Music Player")
label.pack()

listbox = Listbox (root,yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side="right", fill="y")
listbox.pack(side="left",fill="both", expand=True)

for items in names:

    listbox.insert(END,items)
    #inserts each element of songs into listbox to be shown to user

playbutton = Button(root, text="Play")
playbutton.pack()
playbutton.bind("<Button-1>",playsong)

skipbutton = Button(root, text="Skip")
skipbutton.pack()
skipbutton.bind("<Button-1>",skipsong)

backbutton = Button(root, text="Back")
backbutton.pack()
backbutton.bind("<Button-1>",backsong)

stopbutton = Button (root, text="Stop")
stopbutton.pack()
stopbutton.bind("<Button-1>",stopsong)

songlabel.pack()
artistlabel.pack()
albumlabel.pack()


listbox.bind('<<ListboxSelect>>',onselect)

root.mainloop()