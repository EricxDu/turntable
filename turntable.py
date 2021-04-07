'''
Copyright 2021 Eric Duhamel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import os
import random
import re
import time
from mplayer import Player, Step
from os import path, walk

class TurnTable():
    def __init__(self, username=""):
        ''' Initialize the player and album collection '''
        self.p = Player("-joystick -ao alsa")
        # generate the list of albums
        list = []
        homedir = "~" + username
        home = path.expanduser(path.join(homedir, "Music"))
        for root, dirs, files in walk(home):
            for name in files:
                if(name.endswith(".m3u")):
                    list.append(os.path.join(root, name))
        print("Here is my album collection.")
        for album in list:
            print(album)
        self.albums_list = tuple(list)
        self.album = random.randint(0, len(list)-1)
        print("I'm picking one at random: " + list[self.album])

    def minus(self):
        self.p.volume = Step(-10)

    def next(self):
        ''' Start playing the next album '''
        self.album = (self.album + 1)%len(self.albums_list)
        self.p.loadlist(self.albums_list[self.album])

    def play(self):
        ''' Initialize the slave and start playing '''
        self.p.loadlist(self.albums_list[self.album])
        self.p.pause()

    def plus(self):
        self.p.volume = Step(10)

    def skip(self):
        ''' Skip the current track '''
        self.p.time_pos = self.p.length

    def get_alb(self):
        fullname = self.p.filename or ""
        filename = fullname.split(".")[0]
        credits = filename.split("-")[0]
        names = re.split("_",credits)
        name = names[0]
        return name

    def get_art(self):
        fullname = self.p.filename or ""
        filename = fullname.split(".")[0]
        credits = filename.split("-")[0]
        names = re.split("_",credits)
        names.pop(0)
        name = " ".join(names)
        return name

    def get_name(self):
        fullname = self.p.filename or ""
        filename = fullname.split(".")[0]
        names = re.split("-",filename)
        names = re.split("_",names[len(names)-1])
        name = " ".join(names)
        return name

    def get_pos(self, length=10, prog=":", bars="-"):
        perc = self.p.percent_pos or 0
        factor = 100/length
        pos = int(perc/factor)
        slider = ""
        for x in range(length):
            if pos == x:
                slider += prog
            else:
                slider += bars
        return slider

    def get_time(self):
        time_pos = int(self.p.time_pos or 0)
        time = str(int(time_pos/60)) + "m" + str(int(time_pos%60)) + "s"
        length = self.p.length or 0
        long = str(int(length/60)) + "m" + str(int(length%60)) + "s"
        time = time + " / " + long
        return time

    def get_vol(self):
        vol = int(self.p.volume or 0)
        return str(vol) + "%"
