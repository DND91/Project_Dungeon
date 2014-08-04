#!/usr/bin/python
import sfml as sf
import gui.gui_screen as gscr
import gui.gui_button as btn

class GuiTestScreen(gscr.GuiScreen):
    def __init__(self):
        super().__init__(100,100,400,400)
        self.backButton = btn.GuiButton(110, 150, "Back")
        self.gui_list.append(self.backButton)
        
    
    def innerMouseClick(self, game, object, screen, rect):
        if self.backButton == object:
            game.next = screen.lastScreen
            game.window.view = game.window.default_view

