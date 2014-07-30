#!/usr/bin/python
import sfml as sf

def worldToScreen(v):
    return sf.Vector2((2.0*v.x - 2.0*v.y)/4.0, (v.x + v.y)/4.0)

def screenToWorld(v):
    return sf.Vector2((v.x+2.0*v.y)/1.0, (2.0*v.y-v.x)/1.0)

class IsometricTile:
    radius = 16
    
    def __init__(self, body, x, y, game, floor, roof, left, right):
        y += 32
        #x -= 32
        if floor:
            texture = game.textures.fetch("NONE_FLOOR")
            self.floor = sf.Sprite(texture)
            self.floor.position = sf.Vector2(x,y)
            texture2 = game.textures.fetch("ACTIVE_FLOOR")
            self.active_floor = sf.Sprite(texture2)
            self.active_floor.position = sf.Vector2(x,y)
        else:
            self.floor = 0
            self.active_floor = 0
        
        if roof:
            texture = game.textures.fetch("NONE_ROOF")
            self.roof = sf.Sprite(texture)
            self.roof.position = sf.Vector2(x,y-31)
        else:
            self.roof = 0
        if left:
            texture = game.textures.fetch("NONE_WALLS")
            self.left = sf.Sprite(texture)
            self.left.position = sf.Vector2(x,y-15)
            self.left.texture_rectangle = sf.Rectangle((0,0),(32,47))
        else:
            self.left = 0
        
        if right:
            texture = game.textures.fetch("NONE_WALLS")
            self.right = sf.Sprite(texture)
            self.right.position = sf.Vector2(x+32,y-15)
            self.right.texture_rectangle = sf.Rectangle((32,0),(32,47))
        else:
            self.right = 0
        
        self.x = x
        self.y = y
        self.body = body
        self.active = False
    
    def draw(self, ps, game):
        if self.floor != 0 and ps == 0:
            if self.active:
                game.window.draw(self.active_floor)
                self.active = False
            else:
                game.window.draw(self.floor)
        if self.roof != 0 and ps == 1:
            game.window.draw(self.roof)
        if self.left != 0 and ps == 1:
            game.window.draw(self.left)
        if self.right != 0 and ps == 1:
            game.window.draw(self.right)
    