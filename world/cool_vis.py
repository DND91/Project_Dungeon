#!/usr/bin/python
import sfml as sf
import functools
import world.cool_math as cm

class VisBody:
    def __init__(self, owner, ani, ps):
        self.owner = owner
        self.ps = ps
        self.ani = ani
        
    
    def getPass(self):
        return self.ps




class VisWorld:
    def __init__(self, physWorld):
        self.physWorld = physWorld
        self.drawList = [set(), set(), set(), set()]
    
    
    def draw(self, world, game):
        #BUILD DRAW LIST
        for l in self.drawList:
            l.clear()
        
        pPos = game.player.body.rectangle.position
        pPos = self.physWorld.coordsToTile(pPos)
        tile = self.physWorld.getTile(pPos.x, pPos.y)
        tPos = self.physWorld.coordsToTile(tile.rectangle.position)
        
        r = 10
        checkedChunk = list()
        x = pPos.x * 64 - r * 64
        y = pPos.y * 64 - r * 64
        viewRectangle = sf.Rectangle((x,y),(2 * r * 64, 2 * r * 64))
        for x in range(pPos.x-r, pPos.x+r):
            for y in range(pPos.y-r, pPos.y+r):
                tile = self.physWorld.getTile(x, y)
                if not (tile == None) and not (tile == 0):
                    if tile.shallDraw(game):
                        self.drawList[tile.getPass()].add(tile)
                    if not (tile.chunk in checkedChunk):
                        checkedChunk.append(tile.chunk)
                        for body in tile.chunk.bodies:
                            if cm.intersectsRect(viewRectangle, body.rectangle):
                                self.drawList[body.owner.getPass()].add(body.owner)
        
        #self.drawList[game.player.getPass()].add(game.player)
        #SORT LIST
        
        def compare(a, b):
            return (a.rectangle.position.y + a.rectangle.position.x) - (b.rectangle.position.y + b.rectangle.position.x)
        
        for li in self.drawList:
            l = sorted(li, key=functools.cmp_to_key(compare))
            for draweble in l:
                draweble.draw(game)