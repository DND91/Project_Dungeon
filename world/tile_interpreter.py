#!/usr/bin/python

import world.tile_handler as th
import gui.gui_tavern_portal as gtp
import gui.gui_home_portal as ghp
import world.isometric_tile as iso

class TileInfo:
    def __init__(self, char, solid,floor, roof, left, right, tileHandler, transparent = True):
        self.char = char
        self.floor = floor
        self.roof = roof
        self.left = left
        self.right = right
        self.tileHandler = tileHandler
        self.solid = solid
        self.transparent = transparent


class TileInterpreter:
    def __init__(self, game,gameMap):
        self.name = "TERPER!"
        self.game = game
        self.gameMap = gameMap
    
    def construe(self, x, y, pos):
        char = self.gameMap.grid[y][x]
        tileInfo = None
        if char == "#": #BLOCK
            tileInfo = TileInfo("#", True, "", "NONE_ROOF", "NONE_WALLS", "NONE_WALLS", th.TileHandler())
        elif char == "D": #DOOR
            pos2 = iso.worldToScreen(pos)
            drawTile = iso.IsometricTile(0, pos2.x, pos2.y, self.game, "OPEN_DOOR", "", "", "", False)
            tileInfo = TileInfo("D", True, "", "CLOSED_DOOR", "", "", th.MassReverseTile(drawTile), False)
        elif char == "P": #WORLD PORTAL
            pos2 = iso.worldToScreen(pos)
            gui = gtp.GuiTavernPortal()
            
            oth = th.OpenGUIScreenTile(gui)
            tileInfo = TileInfo("P", True, "", "PORTAL", "", "", oth)
        elif char == "H": #HOME PORTAL
            pos2 = iso.worldToScreen(pos)
            gui = ghp.GuiHomePortal()
            
            oth = th.OpenGUIScreenTile(gui)
            tileInfo = TileInfo("P", True, "", "PORTAL", "", "", oth)
        elif char == " ": #EMPTY
            tileInfo = TileInfo(" ", False, "NONE_FLOOR", "", "", "", th.TileHandler())
        
        return tileInfo



