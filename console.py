#!/usr/bin/env python3
# Copyright 2021 Eric Duhamel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
    This module provides a minimal interface based on TurnTable. It
    provides a class with generic methods providing of a few lines of
    information (material) in the form of a text string, and a list of
    commands (controls) in the form of method names.

    To access the minimal interface, instantiate class "Main" and use
    method "get_controls" to retrieve a list of methods to call for
    control, and use method "get_material" to retrieve a string of
    information to display.
"""
import os
import random
import sys

from mplayer import Player

def main():
    """
    This is a basic reference implementation. It demonstrates how to use
    the "Main" class and create a basic user interface.
    """
    main = Main()
    command = ''
    while not command == "quit":
        print("[INFO]")
        print(main.get_material())
        print()
        print("COMMANDS:", main.get_controls())
        command = input("Enter command: ")
        if hasattr(main, command):
            eval("main." + command + "()")

class Main(Player):
    """Create and control music player in background.

    This is a process control class. It abstracts the running of an
    application on the backend and presents information and controls
    in the form of generic lists. Frontends can interface with this
    class by instantiating "Main" as an object, presenting the
    information and controls, and calling the command methods.
    """

    def __init__(self, dirname='~/Music'):
        self.albums = None
        self.cmdlist = ("new", "play", "next", "info")
        self.infolist = ("no album",)
        self.dirname = dirname
        self.new()

    def get_controls(self):
        return ["new", "play", "next", "info"]

    def get_material(self):
        self.info()
        return "\n".join(self.infolist)

    def info(self):
        """Find and put track metadata into the information list."""
        if hasattr(self, "metadata") and self.metadata != None:
            self.infolist = (
                    self.metadata['Album'],
                    self.metadata['Title'],
                    self.metadata['Artist'],
                    self.time_pos)
        elif hasattr(self, "filename") and self.filename != None:
            filename = os.path.splitext(self.filename)[0]
            sort, fullname = filename.split('_', 1)
            art, name = fullname.split("-")
            if hasattr(self, "time_pos") and self.time_pos != None:
                time = int(self.time_pos)
            else:
                time = 0
            time = str(int(time/60)) + 'm' + str(int(time%60)) + 's'
            self.infolist = (sort, art, name, time)

    def new(self):
        """Randomly choose a new album to play."""
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
        self.info()

    def next(self):
        """Skip to the next track in the album."""
        self.pt_step(1)
        self.info()

    def play(self):
        """Pause the music, or play if already paused."""
        self.pause()


if __name__ == '__main__':
    try: main()
    except: sys.exit()
