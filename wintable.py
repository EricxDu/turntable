import sys
import time
import tkinter as tk

import turntable

path = len(sys.argv) > 1 and sys.argv[1] or '~/Music'

player = turntable.TurnTable(path)

def skip_track(event):
    player.skip()

skip = tk.Button(text='skip')
skip.bind('<Button-1>', skip_track)
name = tk.Label()
art = tk.Label()
alb = tk.Label()
vol = tk.Label()
play = tk.Label()
prog = tk.Label()
skip.pack(side=tk.RIGHT)
name.pack(anchor=tk.W)
art.pack(anchor=tk.W)
alb.pack(anchor=tk.W)
vol.pack(anchor=tk.W)
play.pack(anchor=tk.W)
prog.pack(anchor=tk.W)

def main():
    name.config(text='"' + player.get_name() + '"')
    art.config(text=player.get_art())
    alb.config(text=player.get_alb())
    vol.config(text=player.get_vol())
    play.config(text=player.get_time())
    prog.config(text=player.get_prog(50))
    play.after(100, main)

if player.albums != None:
    player.play()
    main()
    play.mainloop()
else:
    sys.exit()
