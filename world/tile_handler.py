#!/usr/bin/python

class TileHandler:
    
    def __init__(self):
        self.tile = 0
        
    def setup(self, tile):
        self.tile = tile
    
    def mouseClick(self, game, object, rect):
        print("TILE FOUND!")
        
    
    def entCollistion(self):
        x = 0

class ActivationTile(TileHandler):
    
    def __init__(self, drawTile):
        super().__init__()
        self.drawTile = drawTile
    
    
    def setup(self, tile):
        self.tile = tile
        self.drawTile.body = tile
    
    def mouseClick(self, game, object, rect):
        #self.tile.drawTile.active = not self.tile.drawTile.active
        self.tile.drawTile, self.drawTile = self.drawTile, self.tile.drawTile

class MassReverseTile(TileHandler):
    def __init__(self, tileInfo):
        super().__init__()
        self.info = tileInfo
        self.info.tileHandler = self
    
    def setup(self, tile):
        self.tile = tile
    
    def mouseClick(self, game, object, rect):
        #self.tile.drawTile.active = not self.tile.drawTile.active
        self.tile.info, self.info = self.info, self.tile.info
        x = self.tile.drawTile.realX
        y = self.tile.drawTile.realY
        self.tile.drawTile.__init__(self.tile, x,y, game)

class OpenGUIScreenTile(TileHandler):
    
    def __init__(self, gui):
        super().__init__()
        self.gui = gui
    
    def setup(self, tile):
        self.tile = tile
    
    def mouseClick(self, game, object, rect):
        if game.current.gui_screen == None:
            game.current.gui_screen = self.gui

















