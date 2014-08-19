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
    
    def draw(self, ps, game):
        if game.player == 0:
            if self.isFloor and ps == 0:
                game.window.draw(self.sprite)
            elif not self.isFloor and ps == 1:
                game.window.draw(self.sprite)
        else:
            if self.isFloor and ps == 0:
                game.window.draw(self.sprite)
            elif not self.isFloor and ps == 1:
                #color = sf.Color(255, 255, 255, 255)
                #if (cm.intersectsRect(self.body.shadowRectangle, game.player.sprite.global_bounds)) and self.transparent:
                #    color = sf.Color(255, 255, 255, 50)
                
                #self.sprite.color = color
                #pv = game.player.sprite.position.x + game.player.sprite.position.y - 64
                #tv = self.sprite.position.x + self.sprite.position.y
                if self.sprite.global_bounds.bottom < game.player.sprite.global_bounds.top or not self.transparent:
                    game.window.draw(self.sprite)
            
            
            























