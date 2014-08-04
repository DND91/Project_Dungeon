#!/usr/bin/python
import sfml as sf

class TextureDatabase:
    database = dict()
    
    def __init__(self):
        self.load_all()
    
    def load_all(self):
        self.load("NONE", "./resources/noneCube.png")
        self.load("NONE_FLOOR", "./resources/notextureIsometric.png")
        self.load("ACTIVE_FLOOR", "./resources/active_tile.png")
        self.load("NONE_WALLS", "./resources/wallsIsometric.png")
        self.load("NONE_ROOF", "./resources/roofIsometric.png")
        self.load("HORSE", "./resources/horse.png")
        self.load("BALL", "./resources/ballCube.png")
        self.load("SOLID", "./resources/solidCube.png")
        self.load("PLAYER", "./resources/playerCube.png")
        self.load("OPEN_DOOR", "./resources/open_door.png")
        self.load("CLOSED_DOOR", "./resources/closed_door.png")
        self.load("ITEM_TILE", "./resources/itemTile.png")
        self.load("HUMAN", "./resources/humanCube.png")
        self.load("ORC", "./resources/orcCube.png")
        self.load("SKELETON", "./resources/skeletonCube.png")
    
    def load(self, name, path):
        try:
           texture = sf.Texture.from_file(path)
           self.database[name] = texture
        except IOError:
            print("FAILED TO LOAD '" + name + "' ON PATH '" + path)
    
    
    def fetch(self, name):
        if name in self.database.keys():
            return self.database[name]
        else:
            return self.database["NONE"]
    
    def clear(self):
        self.database.clear()
        self.load_all()