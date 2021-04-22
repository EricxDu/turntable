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
    if len(sys.argv) > 1:
        player = TurnTable(sys.argv)
    else:
        player = TurnTable()
    done = False
    while not done:
        command = input('Enter command: ')
        if command == 'alb':
            print(player.get_alb())
        elif command == 'art':
            print(player.get_art())
        elif command == 'long':
            print(player.get_long())
        elif command == 'name':
            print(player.get_name())
        elif command == 'prog':
            print(player.get_prog())
        elif command == 'skip':
            print(player.skip())
        elif command == 'sort':
            print(player.get_sort())
        elif command == 'time':
            print(player.get_time())
        elif command == 'vol':
            print(player.get_vol())
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
        print('turntable: here is your album collection ')
        for path in list:
            print(path)
        if len(list) < 1:
            print('turntable: no album collection found')
            print('turntable: try putting some .m3u playlist files in '
                  + dirname)
        else:
            # TODO: check if mplayer exists
            print('turntable: picking a random album... ')
            path = random.choice(list)
            print('turntable: playing ' + path)
            self.p = Player('-joystick -loop 0 -playlist ' + path)

    def get_alb(self):
        path = self.p.path or ''
        name = os.path.basename(os.path.dirname(path))
        return name

    def get_art(self):
        """Return artist name from filename

        Assume name starts at the second string in the split and ends
        after the splitting character changes.
        """
        name = os.path.splitext(self.p.filename or '')[0]
        separators = ' |-|\.|_'
        name = re.split(separators, name, 1)[1]  # discard sorting string
        # find the first and second separators in name
        sep1 = re.findall(separators, name)[0]
        research = ''.join(name.split(sep1))
        sep2 = re.findall(separators, research)[0]
        # artist name ends after second separator
        name = name.split(sep2)[0]
        name = ' '.join(re.split(separators, name))
        return name

    def get_name(self):
        """Return song name from filename

        Assume name is separated by the same character in the last
        parts of the filename.
        """
        name = os.path.splitext(self.p.filename or '')[0]
        separators = ' |-|\.|_'
        name = re.split(separators, name, 1)[1]  # discard sorting string
        # find the last and prelast separators in name
        sep1 = re.findall(separators, name)[-1]
        research = ''.join(name.split(sep1))
        sep2 = re.findall(separators, research)[-1]
        # artist name starts after penultimate separator
        name = name.split(sep1)[1]
        name = ' '.join(re.split(separators, name))
        return name

    def get_sort(self):
        """Return sorting string from filename

        Assume the first string in the split is the sort.
        """
        name = os.path.splitext(self.p.filename or '')[0]
        separators = ' |-|\.|_'
        sort = re.split(separators, name)[0]
        return sort

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
