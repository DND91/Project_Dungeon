#!/usr/bin/python
import sfml as sf
import gui.gui_screen as gscr
import gui.gui_button as btn

class GuiHomePortal(gscr.GuiScreen):
    def __init__(self):
        super().__init__(212,50,600,400)
        gridSize = 64
        
        self.home_button = btn.GuiButton(gridSize * 7, gridSize * 4, "Go Home")
        self.gui_list.append(self.home_button)
        
        self.home = 0
        
    
    def innerMouseClick(self, game, object, screen, rect):
        if self.home_button == object:
            screen.playGui.goHome = True
            
