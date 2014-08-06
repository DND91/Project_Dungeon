#!/usr/bin/python
import sfml as sf
import gui.gui_screen as gscr
import gui.gui_button as btn
from gui.screen import LoadWorldScreen

class GuiTavernPortal(gscr.GuiScreen):
    def __init__(self):
        super().__init__(212,50,600,400)
        gridSize = 64
        self.world1_button = btn.GuiButton(gridSize * 5, gridSize * 4, "World 1")
        self.gui_list.append(self.world1_button)
        
        self.world2_button = btn.GuiButton(gridSize * 7, gridSize * 4, "World 2")
        self.gui_list.append(self.world2_button)
        
        self.world3_button = btn.GuiButton(gridSize * 9, gridSize * 4, "World 3")
        self.gui_list.append(self.world3_button)
        
    
    def innerMouseClick(self, game, object, screen, rect):
        if self.world1_button == object:
            print("World 1")
            game.next = LoadWorldScreen(game, worldSize = 2)
        elif self.world2_button == object:
            print("World 2")
            game.next = LoadWorldScreen(game, worldSize = 4)
        elif self.world3_button == object:
            print("World 3")
            game.next = LoadWorldScreen(game, worldSize = 8)
            

