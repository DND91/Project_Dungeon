#!/usr/bin/python

import world.tile_handler as th
import gui.gui_tavern_portal as gtp
import gui.gui_home_portal as ghp
import world.isometric_tile as iso

class TileInfo:
    def __init__(self, char, tileHandler, txt, solid = False, isFloor = True, transparent = False):
        self.char = char
        self.txt = txt
        self.isFloor = isFloor
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
        if char == "#": #WALL
            tileInfo = TileInfo("#", th.TileHandler(), "STONE_WALL", True, False, True)
        elif char == "D": #DOOR
            pos2 = iso.worldToScreen(pos)
            oInfo = TileInfo(" ", 0, "OPEN_DOOR")
            tileInfo = TileInfo("D", th.MassReverseTile(oInfo), "CLOSED_DOOR", True, False)
        elif char == "P": #WORLD PORTAL
            pos2 = iso.worldToScreen(pos)
            gui = gtp.GuiTavernPortal()
            oth = th.OpenGUIScreenTile(gui)
            tileInfo = TileInfo("P", oth, "PORTAL", True, False)
        elif char == "H": #HOME PORTAL
            pos2 = iso.worldToScreen(pos)
            gui = ghp.GuiHomePortal()
            
            oth = th.OpenGUIScreenTile(gui)
            tileInfo = TileInfo("P", oth, "PORTAL", True, False)
        elif char == " ": #EMPTY
            tileInfo = TileInfo(" ", th.TileHandler(), "NONE_FLOOR")
        
        return tileInfo



