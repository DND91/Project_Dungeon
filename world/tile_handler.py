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
    def __init__(self, drawTile):
        super().__init__()
        self.drawTile = drawTile
    
    def setup(self, tile):
        self.tile = tile
        self.drawTile.body = tile
    
    def mouseClick(self, game, object, rect):
        #self.tile.drawTile.active = not self.tile.drawTile.active
        self.tile.drawTile, self.drawTile = self.drawTile, self.tile.drawTile
        self.tile.info.solid = not self.tile.info.solid