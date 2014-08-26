#!/usr/bin/python
import sfml as sf
import database.animation_database as vis

import os
import glob

window = sf.RenderWindow(sf.VideoMode(1024, 640), "Project: DUNG!", sf.window.Style.CLOSE, sf.ContextSettings(0,0,0,2,0))

database = vis.AnimationDatabase()
database.print()

while True:
    for event in window.events:
        if type(event) is sf.CloseEvent:
            window.close()
            running = False
        elif type(event) is sf.FocusEvent:
            if event.gained:
                pause = False
            elif event.lost:
                pause = True
    
    window.clear(sf.Color.BLACK)
    
    window.display()
