#!/usr/bin/python
import sfml as sf
import math
import random
import world.isometric_tile as iso
import game as game
import functools
from world.cool_math import *
import world.tile_handler as th

class PhysBody:
    
    def __init__(self, owner, x, y, width, height):
        self.owner = owner
        self.rectangle = sf.Rectangle((x,y),(width,height))
        self.velocity = sf.Vector2(0,0)
        self.mass = 100
        self.chunks = []
    

class TileInfo:
    def __init__(self, char, solid,floor, roof, left, right, tileHandler):
        self.char = char
        self.floor = floor
        self.roof = roof
        self.left = left
        self.right = right
        self.tileHandler = tileHandler
        self.solid = solid
    

class PhysTile:
    #Tile Size, Coors per Tile
    tileSize = 64
    
    def __init__(self, chunk, x, y, tileInfo):
        self.rectangle = sf.Rectangle((x,y),(self.tileSize,self.tileSize))
        self.chunk = chunk
        self.info = tileInfo
        
        pos = iso.worldToScreen(self.rectangle.position)
        self.drawTile = iso.IsometricTile(self, pos.x, pos.y, game.Game, self.info.floor, self.info.roof, self.info.left, self.info.right)
        self.tileHandler = self.info.tileHandler
        self.tileHandler.setup(self)
    
    def draw(self, ps, game):
        self.drawTile.draw(ps, game)

class PhysChunk:
    #Chunk Size, Tiles per Chunk
    chunkSize = 8
    
    pixelSize = PhysTile.tileSize * chunkSize
    
    #Want chunk coordinates. Will calculate chunk pos.
    def __init__(self, x, y):
        self.position = sf.Vector2(x,y)
        size = PhysTile.tileSize * self.chunkSize
        self.rectangle = sf.Rectangle((x*size,y*size),(size,size))
        self.bodies = set()
        self.draweble = []
        
        self.tiles = [[0 for xx in range(self.chunkSize)] for xx in range(self.chunkSize)]
        for tileY in range(self.chunkSize):
            for tileX in range(self.chunkSize):
                pos = sf.Vector2(self.rectangle.left + tileX * PhysTile.tileSize, self.rectangle.top + tileY * PhysTile.tileSize)
                if x == 0 and y == 0:
                    tileInfo = TileInfo("_", False,"NONE_FLOOR", "", "", "", th.TileHandler())
                    self.tiles[tileY][tileX] = PhysTile(self, pos.x, pos.y, tileInfo)
                else:
                    if random.randint(0,10) == 0: #BLOCK
                        tileInfo = TileInfo("#", True, "", "NONE_ROOF", "NONE_WALLS", "NONE_WALLS", th.TileHandler())
                        self.tiles[tileY][tileX] = PhysTile(self, pos.x, pos.y, tileInfo)
                    elif random.randint(0,10) == 0: #DOOR
                        pos2 = iso.worldToScreen(pos)
                        drawTile = iso.IsometricTile(0, pos2.x, pos2.y, game.Game, "OPEN_DOOR", "", "", "")
                        tileInfo = TileInfo("#", True, "", "CLOSED_DOOR", "", "", th.MassReverseTile(drawTile))
                        self.tiles[tileY][tileX] = PhysTile(self, pos.x, pos.y, tileInfo)
                    else: #EMPTY
                        tileInfo = TileInfo("_", False, "NONE_FLOOR", "", "", "", th.TileHandler())
                        self.tiles[tileY][tileX] = PhysTile(self, pos.x, pos.y, tileInfo)
                self.draweble.append(self.tiles[tileY][tileX])
        def compare(a, b):
            return (a.rectangle.position.y + a.rectangle.position.x) - (b.rectangle.position.y + b.rectangle.position.x)
        self.draweble.sort(key=functools.cmp_to_key(compare))
        
    
    def info(self):
        print("Chunk: ", self.position)
        print("Boundbox: ", self.rectangle)
        print("Bodies: ", len(self.bodies))
        for y in self.tiles:
            for tile in y:
                print(tile.char, end='')
            print("")
    
    def add(self, body):
        self.bodies.add(body)
    
    def remove(self, body):
        self.bodies.discard(body)
    
    def draw(self, ps, drawList, rect):
        #drawList.extend(self.draweble)
        for dra in self.draweble:
            if intersects(dra, rect):
                drawList.add(dra)
        for dra in self.bodies:
            if intersects(dra, rect):
                drawList.add(dra.owner)

class PhysWorld:
    
    
    #Number of chunks in the world
    worldSize = 8
    
    def __init__(self):
        size = self.worldSize * PhysTile.tileSize * PhysChunk.chunkSize
        self.rectangle = sf.Rectangle((0,0),(size,size))
        self.bodies = set()
        self.chunks = []
        
        
        for y in range(self.worldSize):
            self.chunks.append([])
            for x in range(self.worldSize):
                self.chunks[y].append(PhysChunk(x,y))
        tile = self.chunks[0][0].tiles[5][5]
        
    
    def coordsToChunk(self, vec):
        return sf.Vector2(math.floor(vec.x/PhysChunk.pixelSize), math.floor(vec.y/PhysChunk.pixelSize))
    
    def addBody(self, body):
        self.bodies.add(body)
        self.calculateChunks(body)
    
    def removeBody(self, body):
        self.removeFromChunks(body)
        self.bodies.discard(body)
    
    def removeFromChunks(self, body):
        for colum in body.chunks:
            for chunk in colum:
                if not (chunk == 0):
                    self.chunks[chunk.y][chunk.x].remove(body)
    
    def getTilesInBody(self, body):
        tiles = []
        for chunks in self.chunks:
            for chunk in chunks:
                if intersects(chunk, body):
                    for tile_colum in chunk.tiles:
                        for tile in tile_colum:
                            if intersects(tile, body):
                                tiles.append(tile)
        return tiles
    
    def getBodiesInBody(self, body):
        bodies = []
        for chunks in self.chunks:
            for chunk in chunks:
                if intersects(chunk, body):
                    for body2 in chunk.bodies:
                        if intersects(body2, body):
                            bodies.append(body2)
        return bodies
    
    def calculateChunks(self, body):
        self.removeFromChunks(body)
        xSize = math.ceil(body.rectangle.width / PhysChunk.pixelSize) + 1
        ySize = math.ceil(body.rectangle.height / PhysChunk.pixelSize) + 1
        anchor = self.coordsToChunk(body.rectangle.position)
        
        body.chunks = [[0 for x in range(ySize)] for x in range(xSize)]
        
        if self.worldSize <= (anchor.x + xSize):
            diff = (anchor.x + xSize) - self.worldSize
            anchor.x -= diff
        
        if self.worldSize <= (anchor.y + ySize):
            diff = (anchor.y + ySize) - self.worldSize
            anchor.y -= diff
        
        for y in range(ySize):
            for x in range(xSize):
                if intersects(self.chunks[anchor.y + y][anchor.x + x], body):
                    body.chunks[y][x] = sf.Vector2(anchor.x + x, anchor.y + y)
                    self.chunks[anchor.y + y][anchor.x + x].add(body)
        
    
    def worldLock(self, body):
        if not (contains(self, body)):
            l, t, w, h = body.rectangle
            if l < self.rectangle.left:
                l = self.rectangle.left
            if self.rectangle.right < (l+w):
                l = self.rectangle.right - w
            if t < self.rectangle.top:
                t = self.rectangle.top
            if self.rectangle.bottom < (t+h):
                t = self.rectangle.bottom - h
            body.rectangle.__init__((l, t), (w, h))
        
    def chunkdate(self, body):
        top = body.rectangle.top
        bottom = body.rectangle.bottom
        left = body.rectangle.left
        right = body.rectangle.right
        
        pos = sf.Vector2(left, top)
        topLeftAnchor = self.coordsToChunk(pos)
        
        pos.x = right
        topRightAnchor = self.coordsToChunk(pos)
        
        pos.y = bottom
        bottomRightAnchor = self.coordsToChunk(pos)
        
        pos.x = left
        bottomLeftAnchor = self.coordsToChunk(pos)
        
        def chunkTest(body, y, x, anchor):
            return not (body.chunks[y][x] == anchor)
        
        if chunkTest(body, 0,0, topLeftAnchor) or chunkTest(body, -1,0, bottomLeftAnchor) or chunkTest(body, 0,-1, topRightAnchor) or chunkTest(body, -1,-1, bottomRightAnchor):
            self.calculateChunks(body)
    
    def moveBody(self, body, delta):
        l, t, w, h = body.rectangle
        l += body.velocity.x * delta * PhysTile.tileSize
        t += body.velocity.y * delta * PhysTile.tileSize
        body.rectangle.__init__((l, t), (w, h))
    
    def tileBody(self, body):
        for colum in body.chunks:
            for chunk in colum:
                if not (chunk == 0):
                    #Tile collistion
                    for y in self.chunks[chunk.y][chunk.x].tiles:
                        for tile in y:
                            if intersects(body, tile):
                                if tile.info.solid:
                                    g = gap(tile, body)
                                    l, t, w, h = body.rectangle
                                    if math.fabs(g.x) <= math.fabs(g.y):
                                        l += g.x
                                    else:
                                        t += g.y
                                    body.rectangle.__init__((l, t), (w, h))
                                    print("TILE COLLISTION WITH BODY!")
                                #Add Collision Hook For Tiles, Ent Vs Tile
                                tile.drawTile.active = True #FIX! It is activating draw, but not handler
    
    def bodyBody(self, body):
        for colum in body.chunks:
            for chunk in colum:
                if not (chunk == 0):
                    #Body collistion
                    for otherBody in self.chunks[chunk.y][chunk.x].bodies:
                        if not (body == otherBody) and intersects(body, otherBody):
                            light = body
                            heavy = otherBody
                            if heavy.mass < light.mass:
                                light = otherBody
                                heavy = body
                            g = gap(heavy, light)
                            l, t, w, h = light.rectangle
                            if math.fabs(g.x) <= math.fabs(g.y):
                                l += g.x
                            else:
                                t += g.y
                            light.rectangle.__init__((l, t), (w, h))
                            #Add Collision Hook For Entities, Body Vs Body
                            print("BODY COLLISTION WITH BODY!")
                            #light.owner.world.addRemoval(light.owner)
    
    
    def update(self, delta):
        for body in self.bodies:
            #Update Body
            self.moveBody(body, delta)
            self.worldLock(body)
            self.chunkdate(body)
            
            #Check Tiles
            self.tileBody(body)
            self.worldLock(body)
            self.chunkdate(body)

            #Check Bodies
            self.bodyBody(body)
            self.worldLock(body)
            self.chunkdate(body)
    
    def draw(self, ps, drawList, rect):
        for row in self.chunks:
            for chunk in row:
                if intersects(chunk, rect):
                    chunk.draw(ps, drawList, rect)




#world = PhysWorld()
#body = PhysBody(64*3, 64*3, 64, 64)
#world.addBody(body)
#body.velocity = sf.Vector2(-0.0, 0.5)
#print(body.rectangle)
#for l in range(12):
#    world.update(1)
#    print(body.rectangle)
















