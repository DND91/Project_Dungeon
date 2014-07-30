#!/usr/bin/python
from gui.screen import *
import sfml as sf
from database.texture_database import *

class Game:
    running = True
    pause = False
    current = IntroScreen()
    next = 0
    window = sf.RenderWindow(sf.VideoMode(1024, 640), "Project: DUNG!", sf.window.Style.CLOSE, sf.ContextSettings(0,0,0,2,0))
    offsetX = 0
    offsetY = 0
    textures = TextureDatabase()