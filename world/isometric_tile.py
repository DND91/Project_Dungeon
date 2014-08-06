#!/usr/bin/python
import sfml as sf
import world.cool_math as cm

def worldToScreen(v):
    return sf.Vector2((2.0*v.x - 2.0*v.y)/4.0, (v.x + v.y)/4.0)

def screenToWorld(v):
    return sf.Vector2((v.x+2.0*v.y)/1.0, (2.0*v.y-v.x)/1.0)

class IsometricTile:
    radius = 16
    
    def __init__(self, body, x, y, game, floor, roof, left, right, transparent):
        y += 32
        #x -= 32
        if not (floor == 0 or floor == ""):
            texture = game.textures.fetch(floor)
            self.floor = sf.Sprite(texture)
            self.floor.position = sf.Vector2(x,y)
            texture2 = game.textures.fetch("ACTIVE_" + floor)
            self.active_floor = sf.Sprite(texture2)
            self.active_floor.position = sf.Vector2(x,y)
        else:
            self.floor = 0
            self.active_floor = 0
        
        if not (roof == 0 or roof == ""):
            texture = game.textures.fetch(roof)
            self.roof = sf.Sprite(texture)
            self.roof.position = sf.Vector2(x,y-31)
        else:
            self.roof = 0
        if not (left == 0 or left == ""):
            texture = game.textures.fetch(left)
            self.left = sf.Sprite(texture)
            self.left.position = sf.Vector2(x,y-15)
            self.left.texture_rectangle = sf.Rectangle((0,0),(32,47))
        else:
            self.left = 0
        
        if not (right == 0 or right == ""):
            texture = game.textures.fetch(right)
            self.right = sf.Sprite(texture)
            self.right.position = sf.Vector2(x+32,y-15)
            self.right.texture_rectangle = sf.Rectangle((32,0),(32,47))
        else:
            self.right = 0
        
        self.x = x
        self.y = y
        self.body = body
        self.transparent = transparent
    
    def draw(self, ps, game):
        if game.player == 0 or True:
            if self.floor != 0 and ps == 0:
                game.window.draw(self.floor)
            if self.roof != 0 and ps == 1:
                game.window.draw(self.roof)
            if self.left != 0 and ps == 1:
                game.window.draw(self.left)
            if self.right != 0 and ps == 1:
                game.window.draw(self.right)
        else:
            color = sf.Color(255, 255, 255, 255)
            self.body.rectangle, self.body.shadowRectangle = self.body.shadowRectangle, self.body.rectangle
            if (cm.intersects(self.body, game.player.body)) and self.transparent:
                color = sf.Color(255, 255, 255, 100)
            self.body.rectangle, self.body.shadowRectangle = self.body.shadowRectangle, self.body.rectangle
            
            if self.floor != 0 and ps == 0:
                game.window.draw(self.floor)
            if self.roof != 0 and ps == 1:
                self.roof.color = color
                game.window.draw(self.roof)
            if self.left != 0 and ps == 1:
                self.left.color = color
                game.window.draw(self.left)
            if self.right != 0 and ps == 1:
                self.right.color = color
                game.window.draw(self.right)
            
            
            























