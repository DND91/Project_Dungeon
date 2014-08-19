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
    
    def __init__(self, physWorld):
        self.physWorld = physWorld
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
        
        
        #OBJECTS
        '''
        for t in range(5):
            continue
            x = 0
            y = 0
            
            for r in range(10):
                x = random.randint(1, self.physWorld.worldSize * PhysChunk.chunkSize)
                y = random.randint(1, self.physWorld.worldSize * PhysChunk.chunkSize)
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
        '''
        
        self.drawList = [set(), set(), set(), set()]
        
        
    
    
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
            for l in self.drawList:
                l.clear()
            
            self.physWorld.draw(game, self.drawList, self) #FILL LIST
            self.phys_screen, self.rectangle = self.rectangle, self.phys_screen
            #SORT LIST
            
            def compare(a, b):
                return (a.rectangle.position.y + a.rectangle.position.x) - (b.rectangle.position.y + b.rectangle.position.x)
            
            for li in self.drawList:
                l = sorted(li, key=functools.cmp_to_key(compare))
                for draweble in l:
                    draweble.draw(game)
                    
            
            #DRAW FRAME
            game.window.draw(self.frame)
            game.window.draw(self.toolbar)



















