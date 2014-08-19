#!/usr/bin/python
import sfml as sf
import math
import random
import world.isometric_tile as iso
import game as game
import functools
from world.cool_math import *




class PhysBody:
    
    def __init__(self, owner, x, y, width, height):
        self.owner = owner
        self.rectangle = sf.Rectangle((x,y),(width,height))
        self.velocity = sf.Vector2(0,0)
        self.mass = 100
        self.chunks = []
    
    def getPass(self):
        return self.owner.getPass()

class PhysTile:
    #Tile Size, Coors per Tile
    tileSize = 64
    
    def __init__(self, chunk, x, y, tileInfo):
        self.rectangle = sf.Rectangle((x,y),(self.tileSize,self.tileSize))
        shadowRange = 2 * 64 + 32
        self.shadowRectangle = sf.Rectangle((x-shadowRange,y-shadowRange),(self.tileSize+shadowRange,self.tileSize+shadowRange))
        self.chunk = chunk
        self.info = tileInfo
        
        pos = iso.worldToScreen(self.rectangle.position)
        self.drawTile = iso.IsometricTile(self, pos.x, pos.y, game.Game)
        self.tileHandler = self.info.tileHandler
        self.tileHandler.setup(self)
    
    def draw(self, game):
        self.drawTile.draw(game)
    
    def getPass(self):
        return self.drawTile.getPass()
    
    def shallDraw(self, game):
        return self.drawTile.shallDraw(game)

class PhysChunk:
    #Chunk Size, Tiles per Chunk
    chunkSize = 8
    
    pixelSize = PhysTile.tileSize * chunkSize
    
    #Want chunk coordinates. Will calculate chunk pos.
    def __init__(self, x, y, ti):
        self.position = sf.Vector2(x,y)
        size = PhysTile.tileSize * self.chunkSize
        self.rectangle = sf.Rectangle((x*size,y*size),(size,size))
        self.bodies = set()
        self.draweble = []
        
        tilePos = sf.Vector2(x * self.chunkSize, y * self.chunkSize)
        
        self.tiles = [[0 for xx in range(self.chunkSize)] for xx in range(self.chunkSize)]
        
        for tileY in range(self.chunkSize):
            for tileX in range(self.chunkSize):
                pos = sf.Vector2(self.rectangle.left + tileX * PhysTile.tileSize, self.rectangle.top + tileY * PhysTile.tileSize)
                currentTile = sf.Vector2(tilePos.x + tileX, tilePos.y + tileY)
                
                tileInfo = ti.construe(currentTile.x, currentTile.y, pos)
                
                if not (tileInfo == None):
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
    
    def draw(self, game, drawList, rect):
        for dra in self.draweble:
            if intersects(dra, rect) and dra.shallDraw(game):
                drawList[dra.getPass()].add(dra)
        for dra in self.bodies:
            if intersects(dra, rect):
                drawList[dra.getPass()].add(dra.owner)

class PhysWorld:
    
    
    #Number of chunks in the world
    #worldSize = 8
    
    def __init__(self, ti, worldSize = 8):
        self.worldSize = worldSize
        #PhysWorld Init
        size = self.worldSize * PhysChunk.chunkSize * PhysTile.tileSize
        self.rectangle = sf.Rectangle((0,0),(size,size))
        self.bodies = set()
        self.chunks = []
        
        #Chunk Generation
        for y in range(self.worldSize):
            self.chunks.append([])
            for x in range(self.worldSize):
                self.chunks[y].append(PhysChunk(x,y, ti))
        
    
    def coordsToChunk(self, vec):
        return sf.Vector2(math.floor(vec.x/PhysChunk.pixelSize), math.floor(vec.y/PhysChunk.pixelSize))
    
    #Want Tile x and y position in map
    def getTile(self, x, y):
        chunkX = math.floor(x / self.worldSize)
        chunkY = math.floor(y / self.worldSize)
        tileX = x % PhysChunk.chunkSize
        tileY = y % PhysChunk.chunkSize
        chunkX = min(chunkX, self.worldSize - 1)
        chunkY = min(chunkY, self.worldSize - 1)
        return self.chunks[chunkY][chunkX].tiles[tileY][tileX]
    
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
                            if not (tile == 0) and intersects(tile, body):
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
                            if not (tile == 0) and intersects(body, tile):
                                if tile.info.solid:
                                    g = gap(tile, body)
                                    l, t, w, h = body.rectangle
                                    if math.fabs(g.x) <= math.fabs(g.y):
                                        l += g.x
                                    else:
                                        t += g.y
                                    body.rectangle.__init__((l, t), (w, h))
                                    #print("TILE COLLISTION WITH BODY!")
                                #Add Collision Hook For Tiles, Ent Vs Tile
                                tile.drawTile.active = True #FIX! It is activating draw, but not handler
    
    def bodyBody(self, body):
        for colum in body.chunks:
            for chunk in colum:
                if not (chunk == 0):
                    #Body collistion
                    for otherBody in self.chunks[chunk.y][chunk.x].bodies:
                        if not (body == otherBody) and intersects(body, otherBody):
                            if  body.owner.solid and otherBody.owner.solid:
                                light = body
                                heavy = otherBody
                                if heavy.mass < light.mass and heavy.owner.moviable:
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
                            #print("BODY COLLISTION WITH BODY!")
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
    
    def draw(self, game, drawList, rect):
        for row in self.chunks:
            for chunk in row:
                if intersects(chunk, rect):
                    chunk.draw(game, drawList, rect)




















