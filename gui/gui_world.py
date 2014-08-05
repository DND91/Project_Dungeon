#!/usr/bin/python
import game
import sfml as sf
from gui.gui_object import *
import entity.entity as entity
import entity.entity_item as ientity
import entity.entity_monster as mentity
from world.isometric_tile import *
from world.cool_phys import *
import functools
import bisect
import random
from collections import deque
import item.generator as igen
import entity.monster.generator as mgen

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
        
        
        
        self.remove_queue = deque()
        
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
        for r in range(100000):
            x = random.randint(1, PhysWorld.worldSize * PhysChunk.chunkSize)
            y = random.randint(1, PhysWorld.worldSize * PhysChunk.chunkSize)
            tile = self.physWorld.getTile(x, y)
            if not (tile == 0) and not (tile.info.solid):
                break
        
        self.player = entity.PlayerEntity(self, x*64+5,y*64+5, game.Game)
        self.addEntity(self.player)
        game.Game.player = self.player
        
        #OBJECTS
        for t in range(50):
            x = 0
            y = 0
            
            for r in range(100000):
                x = random.randint(1, PhysWorld.worldSize * PhysChunk.chunkSize)
                y = random.randint(1, PhysWorld.worldSize * PhysChunk.chunkSize)
                tile = self.physWorld.getTile(x, y)
                if not (tile == 0) and not (tile.info.solid):
                    break
            
            if random.randint(0, 5) == 0:
                monster = mentity.MonsterEntity(self, x*64,y*64, game.Game, mgen.generateMonster(50))
                self.addEntity(monster)
            if random.randint(0, 5) == 0:
                ie = ientity.ItemEntity(self, x*64,y*64, game.Game, igen.generateItemStack(50, 1))
                self.addEntity(ie)
            else:
                ball = entity.BallEntity(self, x*64,y*64, game.Game)
                self.addEntity(ball)
        
        
        #ZOOM
        #game.Game.window.view.zoom(10.0)
        self.drawList = set()
        
        
    
    def addEntity(self, entity):    
        self.enteties.append(entity)
        self.physWorld.addBody(entity.body)
    
    def removeEntity(self, entity):
        self.physWorld.removeBody(entity.body)
        self.enteties.remove(entity)
    
    def addRemoval(self, entity):
        self.remove_queue.append(entity)
    
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
        
        try:
            while True:
                ent = self.remove_queue.popleft()
                self.removeEntity(ent)
        except IndexError:
            pass
        except ValueError:
            pass
    
    
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



















