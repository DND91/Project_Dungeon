#!/usr/bin/python
import sfml as sf
import world.cool_math as cm

def worldToScreen(v):
    return sf.Vector2((2.0*v.x - 2.0*v.y)/4.0, (v.x + v.y)/4.0)

def screenToWorld(v):
    return sf.Vector2((v.x+2.0*v.y)/1.0, (2.0*v.y-v.x)/1.0)

class IsometricTile:
    radius = 16
    
    def __init__(self, body, x, y, game):
        isFloor = body.info.isFloor
        text = body.info.txt
        transparent = body.info.transparent
        texture = game.textures.fetch(text)
        self.sprite = sf.Sprite(texture)
        self.realX = x
        self.realY = y
        #y += 32
        #x -= 32
        posistion = sf.Vector2(0,0)
        if isFloor:
            posistion.x = x
            posistion.y = y + 32
        else:
            posistion.x = x
            posistion.y = y + 64 - texture.height
        
        self.sprite.position = posistion
        self.isFloor = isFloor
        
        self.x = x
        self.y = y
        self.body = body
        self.transparent = transparent
        self.ps = 1
        if self.isFloor:
            self.ps = 0
    
    def draw(self, game):
        game.window.draw(self.sprite)
    
    def getPass(self):
        return self.ps
    
    def shallDraw(self, game):
        if self.isFloor:
            return True
        else:
            return self.sprite.global_bounds.bottom < game.player.visPos.y or not self.transparent























