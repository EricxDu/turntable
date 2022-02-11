#!/usr/bin/env python3
"""Copyright 2021 Eric Duhamel

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
"""
import os
import random
import re
import sys
import time

from mplayer import Player

def main():
    player = TurnTable()
    command = ''
    while not command == "quit":
        for info in player.inflist:
            print(info)
        print(player.cmdlist)
        command = input("Enter command: ")
        if hasattr(player, command):
            eval("player." + command + "()")

class TurnTable(Player):
    def __init__(self, dirname='~/Music'):
        self.albums = None
        self.cmdlist = ("new", "stop", "play", "next", "info")
        self.inflist = ("no album",)
        self.dirname = dirname
        self.new()

    def info(self):
        if hasattr(self, "metadata") and self.metadata != None:
            self.inflist = (
                    self.metadata['Album'],
                    self.metadata['Title'],
                    self.metadata['Artist'],
                    self.time_pos)
        else:
            self.inflist = (self.filename.split("-"))

    def new(self):
        if hasattr(self, "_proc"):  # hacky way to make mplayer not crash
            self.stop()
        if self.albums == None:
            dirname = os.path.expanduser(self.dirname)
            self.albums = []
            for name in os.listdir(dirname):
                if(name.endswith('.m3u')):
                    self.albums.append(os.path.join(dirname, name))
        elif len(self.albums) > 0:
            playlist = random.choice(self.albums)
            super().__init__(
                    '-vo null -nolirc -joystick -loop 0 -playlist ' + playlist)
        if hasattr(self, "_proc"):  # hacky way to make mplayer not crash
            self.info()

    def next(self):
        self.pt_step(1)
        time.sleep(1)
        if hasattr(self, "_proc"):  # hacky way to make mplayer not crash
            self.info()

    def play(self):
        self.pause()


if __name__ == '__main__':
    try: main()
    except: sys.exit()
