#!/usr/bin/env python3
'''Copyright 2021 Eric Duhamel

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
import sys
import time
from mplayer import Player

def main():
    print("invocation: " + sys.argv[0])
    if len(sys.argv) > 1:
        path = sys.argv[1]
        print("turntable: searching " + path)
    player = TurnTable(path)
    done = False
    while not done:
        command = input("Enter command: ")
        if command == "alb":
            print(player.get_alb())
        elif command == "art":
            print(player.get_art())
        elif command == "long":
            print(player.get_long())
        elif command == "name":
            print(player.get_name())
        elif command == "prog":
            print(player.get_prog())
        elif command == "time":
            print(player.get_time())
        elif command == "vol":
            print(player.get_vol())
        elif command == "quit":
            done = True

class TurnTable():
    def __init__(self, dirname):
        ''' Initialize the player and album collection '''
        # generate the list of albums
        list = []
        for name in os.listdir(dirname):
            if(name.endswith(".m3u")):
                list.append(os.path.join(dirname, name))
        print("Here is my album collection: ")
        for path in list:
            print(path)
        if len(list) < 1:
            print("No album collection found")
            print("Try putting some .m3u playlist files in " + dirname)
        else:
            # TODO: check if mplayer exists
            path = random.choice(list)
            self.p = Player("-joystick -loop 0 -playlist " + path)

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

    def get_prog(self, length=10, prog=":", bars="-"):
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


if __name__ == "__main__":
    try: main()
    except: sys.exit()
