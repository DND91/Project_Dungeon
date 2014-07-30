#!/usr/bin/python
import game
import sfml as sf
from gui.gui_object import *
import entity.entity as entity
from world.isometric_tile import *
from world.cool_phys import *
import functools
import bisect
import random

def find_fwd_iter(S, i):
    j = bisect.bisect_left(S, i)
    for k in range(j, len(S)):
        yield S[k]

def find_bkwd_iter(S, i):
    j = bisect.bisect_left(S, i)
    for k in range(j, -1, -1):
        yield S[k]

class GuiWorld(GuiObject):
    name = "WORLD"
    frame_color = sf.Color(160, 160, 160)
    
    def __init__(self):
        self.physWorld = PhysWorld()
        self.border = 3
        border = self.border
        width = 1.0
        super().__init__(border,border, game.Game.window.size.x-2*border, game.Game.window.size.y*width-2*border)
        self.frame = sf.RectangleShape()
        self.frame.size = (game.Game.window.size.x-2*border, game.Game.window.size.y*width-2*border)
        self.frame.fill_color = sf.Color.TRANSPARENT
        self.frame.outline_color = self.frame_color
        self.frame.outline_thickness = border
        self.frame.position = (border, border)
        
        self.toolbar = sf.RectangleShape()
        self.toolbar.size = (game.Game.window.size.x, game.Game.window.size.y*0.25)
        self.toolbar.fill_color = self.frame_color
        self.toolbar.outline_color = self.frame_color
        self.toolbar.outline_thickness = border
        self.toolbar.position = (0, game.Game.window.size.y*0.75)
        
        self.enteties = []
        
        #PHYS SCREEN
        mul = 4
        self.phys_screen = sf.Rectangle(screenToWorld(sf.Vector2(0, 0)), (mul * PhysChunk.pixelSize, mul * PhysChunk.pixelSize))
        #start = screenToWorld(sf.Vector2(0,0))
        #end = screenToWorld(sf.Vector2(game.Game.window.size.x*1, game.Game.window.size.y*1))
        #self.rectangle.__init__(start, end-start)
        #for x in range(10):
        #    for y in range(10):
        #        worldPos = worldToScreen(sf.Vector2(x, y))
        #        self.enteties.append(entity.SolidEntity(worldPos.x*16,worldPos.y*16, game.Game))
        
        #PLAYER
        self.player = entity.PlayerEntity(1*64+5,1*64+5, game.Game)
        self.enteties.append(self.player)
        self.physWorld.addBody(self.player.body)
        game.Game.player = self.player
        
        #OBJECTS
        for t in range(50):
            x = random.randint(1, PhysWorld.worldSize * PhysChunk.chunkSize)
            y = random.randint(1, PhysWorld.worldSize * PhysChunk.chunkSize)
            if random.randint(0, 5) == 0:
                self.solid = entity.SolidEntity(x*64,y*64, game.Game)
                self.enteties.append(self.solid)
                self.physWorld.addBody(self.solid.body)
            else:
                self.ball = entity.BallEntity(x*64,y*64, game.Game)
                self.enteties.append(self.ball)
                self.physWorld.addBody(self.ball.body)
        
        
        #ZOOM
        #game.Game.window.view.zoom(10.0)
        self.drawList = set()
        
        
    
    def fillWorld(self, tileList, world):
        y = 0
        for list in world:
            x = 0
            for tile in list:
                worldPos = worldToScreen(sf.Vector2(x, y))
                floor = (tile & 1) == 1
                roof = (tile & 2) == 2
                left = (tile & 4) == 4
                right = (tile & 8) == 8
                tileList.append(IsometricTile(worldPos.x*16, worldPos.y*16, game.Game, floor, roof, left, right))
                x += 1
            y += 1
    
    #def collision(self, mouseRect):
    #    return False
    
    def update(self, game, delta):
        for entity in self.enteties:
            entity.update(game, delta)
        self.physWorld.update(delta)
        self.frame.position = (self.border+game.window.view.center.x-game.window.width/2, self.border+game.window.view.center.y-game.window.height/2)
        self.toolbar.position = (self.border+game.window.view.center.x-game.window.width/2, self.border+game.window.view.center.y-game.window.height/2+game.window.height*0.75)
        l, t, w, h = self.phys_screen
        mul = 0.48
        pos = screenToWorld(sf.Vector2(self.frame.position.x+game.window.width*mul, self.frame.position.y-game.window.height*mul))
        l = pos.x
        t = pos.y
        self.phys_screen.__init__((l, t), (w, h))
        #print(self.phys_screen)
        #for entA in self.enteties:
         #   for entB in self.enteties:
         #       if entA != entB and entA.intersects(entB):
          #          entA.intersectsWith(entB)
    
    def draw(self, pss, game):
        if pss == 0:
            #BUILD DRAW LIST
            self.phys_screen, self.rectangle = self.rectangle, self.phys_screen
            self.drawList.clear()
            #for entity in self.enteties:
                #if intersects(entity.body, self):
                #    self.drawList.append(entity)
                    #entity.draw(ps, game)
            
            self.physWorld.draw(0, self.drawList, self)
            self.phys_screen, self.rectangle = self.rectangle, self.phys_screen
            #SORT DRAW LIST
            def compare(a, b):
                return (a.rectangle.position.y + a.rectangle.position.x) - (b.rectangle.position.y + b.rectangle.position.x)
            l = sorted(self.drawList, key=functools.cmp_to_key(compare))
            
            #DRAW EVERYTHING IN LIST
            for ps in range(6):
                for draweble in l:
                    draweble.draw(ps, game)
            
            game.window.draw(self.frame)
            game.window.draw(self.toolbar)



















