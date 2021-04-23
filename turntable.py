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
    print('invocation: ' + sys.argv[0])
    if len(sys.argv) > 1: player = TurnTable(sys.argv[1])
    else: player = TurnTable()
    done = False
    while not done and player.albums != None:
        print('commands: alb art name play prog skip sort time vol quit')
        command = input('Enter command: ')
        if command == 'alb': print(player.get_alb())
        elif command == 'art': print(player.get_art())
        elif command == 'name': print(player.get_name())
        elif command == 'play': player.play()
        elif command == 'prog': print(player.get_prog())
        elif command == 'skip': player.skip()
        elif command == 'sort': print(player.get_sort())
        elif command == 'time': print(player.get_time())
        elif command == 'vol': print(player.get_vol())
        elif command == 'quit':
            done = True


class TurnTable():
    def __init__(self, dirname='~/Music'):
        """ Initialize the player and album collection """
        # generate the list of albums
        dirname = os.path.expanduser(dirname)
        print('turntable: searching ' + dirname)
        list = []
        for name in os.listdir(dirname):
            if(name.endswith('.m3u')):
                list.append(os.path.join(dirname, name))
        if len(list) > 0:
            print('turntable: here is your music collection ')
            for path in list: print(path)
            self.albums = list
        else:
            print('turntable: no music found')
            print('turntable: try putting some .m3u playlist files in '
                  + dirname)
            self.albums = None
        self.p = None

    def play(self):
        if self.albums != None:
            print('turntable: picking a random album... ')
            playlist = random.choice(self.albums)
            print('turntable: playing ' + playlist)
            if self.p != None: del self.p
            self.p = Player('-nolirc -joystick -loop 0 -playlist ' + playlist)
        else:
            print('turntable: no album collection found')
            print('turntable: try putting some .m3u playlist files')
            print('turntable: in a folder then restart turntable')

    def get_alb(self):
        path = self.p.path or ''
        return os.path.basename(os.path.dirname(path))

    def get_art(self):
        """Return artist name from filename."""
        return self.get_substrings()['art']

    def get_name(self):
        """Return song name from filename."""
        return self.get_substrings()['name']

    def get_prog(self, length=10, prog=':', bars='-'):
        """Return a progress bar

        Format the bar as a string with each character representing
        ten percent of progress, unless otherwise specified.
        """
        perc = self.p.percent_pos or 0
        factor = 100/length
        pos = int(perc/factor)
        slider = ''
        for x in range(length):
            if pos == x:
                slider += prog
            else:
                slider += bars
        return slider

    def get_sort(self):
        """Return sorting string from filename."""
        return self.get_substrings()['sort']

    def get_substrings(self):
        """Split filename into three strings

        Assume everything to the left of first _ is 'sort' string and
        everything to the right of last - is song 'name'. The rest of
        the filename is 'art'ist name. If all else fails, 'sort' and
        'art' can be empty strings. These strings never overlap."""
        filename = os.path.splitext(self.p.filename or '')[0]
        #sep1, sep2 = filename.find('_'), filename.rfind('-')
        sort = filename.split('_', 1)
        art = sort.pop().split('-', 1)
        name = art.pop()
        art = len(art) > 0 and art.pop() or ''
        sort = len(sort) > 0 and sort.pop() or ''
        names = {'sort': sort, 'art': art, 'name': name}
        for n in names:
            names[n] = ' '.join(re.split('-|_', names[n]))
        return names

    def get_time(self):
        """Return song playing time and total time

        Format as two m-s indicators separated by a slash for 'current
        time out of playtime'.
        """
        time_pos = int(self.p.time_pos or 0)
        time = str(int(time_pos/60)) + 'm' + str(int(time_pos%60)) + 's'
        length = self.p.length or 0
        long = str(int(length/60)) + 'm' + str(int(length%60)) + 's'
        time = time + ' / ' + long
        return time

    def get_vol(self):
        """Return system volume as a percentage."""
        vol = int(self.p.volume or 0)
        return str(vol) + '%'

    def skip(self):
        """Skip to end of current track."""
        self.p.time_pos = self.p.length or 0


if __name__ == '__main__':
    try: main()
    except: sys.exit()
