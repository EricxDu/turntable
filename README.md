# Turntable
A friendly Python module that browses your album collection and puts on
a record to listen with you.

## Requirements
Turntable requires mplayer.py and mplayer

* $ pip install mplayer.py
* $ pkcon install mplayer

Turntable is designed to return useful info for you to display using
whichever graphics module you prefer, and running the main module
directly only supports a simple command-line interface. Using the
GUI frontend Wintable requires Tkinter.

* $ pip install tk

## Usage
Turntable looks for .m3u playlist files to load music albums. It
searches the Music folder of your user's directory by default.
Alternatively you can point it at any folder and it will search there.

* $ python3 turntable.py
* $ python3 turntable.py mymusicfolder
* $ python3 wintable.py
* $ python3 wintable.py mymusicfolder

## Notes
At present Turntable parses track name and artist information from the
filename, in case metadata cannot be retrieved from MPlayer. Everything
to the left of the first underscore is considered a sorting string
(e.g. 05, kahvi256a, etc.), and everything to the right of the first
hyphen is considerd the track title. Album name is derived from the root
directory of each file location.

------    ----    ----    ----    ----    ----    ----    ----    ------
