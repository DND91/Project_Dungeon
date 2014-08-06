#!/usr/bin/python
import sfml as sf
from gui.gui_button import *
from gui.gui_text import *
from gui.gui_toys import *
import gui.gui_progressbar as guipb
import world.isometric_tile as iso
import gui.gui_screen as gscr

import gui.gui_test_screen as gtscr
import gui.gui_load_icon as guili
import generate.game_map as gmap


class Screen:
    def __init__(self):
        self.name = "SCREEN"
        self.gui_list = []
        self.gui_screen = None
    
    def event(self, game, event):
        if type(event) is sf.MouseButtonEvent: #Better aiming with mouse click...
            if event.button == sf.Mouse.LEFT and event.released:
                rect = sf.Rectangle(event.position, sf.Vector2(4, 4))
                if not (self.gui_screen == None):
                    if self.gui_screen.collision(rect) and not self.gui_screen.mouseClick(game, self, rect):
                        return
                for object in self.gui_list:
                    if object.collision(rect):
                        if object.mouseClick(game, self, rect):
                            self.mouseClick(game, object, rect)
                        break
        if type(event) is sf.KeyEvent:
            if event.released:
                if event.code == sf.Keyboard.ESCAPE:
                    if not (self.gui_screen == None):
                        self.gui_screen = None
                else:
                    if not (self.gui_screen == None):
                        if not self.gui_screen.keyClick(game, event.code):
                            return
                    if self.keyClick(game, event.code):
                        for object in self.gui_list:
                            object.keyClick(game, self, event.code)
        
    
    def mouseClick(self, game, object, rect):
        x = 0
    
    def keyClick(self, game, code):
        x = 0
        return True
    
    def update(self, game, delta):
        for object in self.gui_list:
            object.update(game, delta)
    
    def draw(self, ps, game):
        for object in self.gui_list:
            object.draw(ps, game)
    

class IntroScreen(Screen):
    
    def __init__(self):
        self.name = "INTRO"
        self.gui_list = []
        self.gui_screen = None
        title = GuiText(10,10, "PROJECT: DUNG!")
        title.text.character_size = 120
        title.text.style = sf.Text.BOLD
        self.gui_list.append(title)
        self.nextButton = GuiButton((1024/2)-(60), 640-50, "Click To Start")
        self.gui_list.append(self.nextButton)
        
    
    def mouseClick(self, game, object, rect):
        if self.nextButton == object:
            game.next = MainMenuScreen(game)





class MainMenuScreen(Screen):
    #playButton = 0
    #optionButton = 0
    #helpButton = 0
    #exitButton = 0
    
    def __init__(self, game):
        self.name = "MAIN_MENU"
        self.gui_list = []
        self.gui_screen = None
        title = GuiText(10,10, "PROJECT: DUNG!")
        title.text.character_size = 32
        title.text.style = sf.Text.BOLD
        self.gui_list.append(title)
        
        space = 30
        self.playButton = GuiButton(10, 50 + space * 0, "Play")
        self.gui_list.append(self.playButton)
        
        self.optionButton = GuiButton(10, 50 + space * 1, "Option")
        self.gui_list.append(self.optionButton)
        
        self.helpButton = GuiButton(10, 50 + space * 2, "Help")
        self.gui_list.append(self.helpButton)
        
        self.exitButton = GuiButton(10, 50 + space * 3, "Exit")
        self.gui_list.append(self.exitButton)
        
        self.load_icon = guili.GuiLoadIcon(game, 512, 320)
        self.gui_list.append(self.load_icon)
    
    def mouseClick(self, game, object, rect):
        if self.playButton == object:
            game.next = LoadWorldScreen(game, "tavern", 2)
        elif self.optionButton == object:
            game.next = OptionScreen(self)
        elif self.helpButton == object:
            game.next = HelpScreen(self)
        elif self.exitButton == object:
            game.running = False

class OptionScreen(Screen):
    
    def __init__(self, lastScreen):
        self.name = "OPTIONS"
        self.gui_list = []
        self.gui_screen = None
        self.lastScreen = lastScreen
        title = GuiText(10,10, "OPTIONS")
        title.text.character_size = 32
        title.text.style = sf.Text.BOLD
        self.gui_list.append(title)
        
        self.backButton = GuiButton(10, 50, "Back")
        self.gui_list.append(self.backButton)
    
    def mouseClick(self, game, object, rect):
        if self.backButton == object:
            game.next = self.lastScreen
            

class HelpScreen(Screen):
    
    def __init__(self, lastScreen):
        self.name = "HELP"
        self.gui_list = []
        self.gui_screen = None
        self.lastScreen = lastScreen
        title = GuiText(10,10, "HELP")
        title.text.character_size = 32
        title.text.style = sf.Text.BOLD
        self.gui_list.append(title)
        
        self.backButton = GuiButton(10, 50, "Back")
        self.gui_list.append(self.backButton)
    
    def mouseClick(self, game, object, rect):
        if self.backButton == object:
            game.next = self.lastScreen

class PlayScreen(Screen):
    
    def __init__(self, game, physWorld, world):
        self.name = "PLAY"
        self.gui_list = []
        self.gui_screen = None
        
        self.title = GuiText(10,10, "PLAY")
        self.title.text.character_size = 32
        self.title.text.style = sf.Text.BOLD
        self.gui_list.append(self.title)
        
        self.menuButton = GuiButton(10, 50, "Menu")
        self.gui_list.append(self.menuButton)
        
        self.playGui = world
        self.gui_list.append(self.playGui)
        game.window.view = sf.View(sf.Rectangle((0, 0), (game.window.width, game.window.height)))
        
    
    def update(self, game, delta):
        super().update(game,delta)
        pos = sf.Vector2(3+game.window.view.center.x-game.window.width/2, 3+game.window.view.center.y-game.window.height/2)
        self.menuButton.position = sf.Vector2(10 + pos.x, 50 + pos.y)
        self.title.position = sf.Vector2(10 + pos.x, 10 + pos.y)
        
    
    
    def mouseClick(self, game, object, rect):
        if self.menuButton == object:
            game.next = MainMenuScreen(game)
            game.window.view = game.window.default_view
        elif self.playGui == object:
            pos = sf.Vector2(game.window.view.center.x-game.window.width/2, game.window.view.center.y-game.window.height/2)
            mouse = sf.Mouse.get_position(game.window)
            pos.x += mouse.x
            pos.y += mouse.y
            pos = iso.screenToWorld(pos)
            n_rect = PhysBody(0, pos.x-64*1.5-2, pos.y-32-2, 4, 4)
            bodies = self.playGui.physWorld.getBodiesInBody(n_rect)
            if 0 < len(bodies):
                for b in bodies:
                    b.owner.mouseClick(game)
                    #INTERACTION HOOK, PLAYER MOUSE VS BODY
            else:
                tiles = self.playGui.physWorld.getTilesInBody(n_rect)
                for t in tiles: #Change to only one
                    t.tileHandler.mouseClick(game, object, rect)
                    #INTERACTION HOOK, PLAYER MOUSE VS TILE
    
    def update(self, game, delta):
        for object in reversed(self.gui_list):
            object.update(game, delta)
        if not (self.gui_screen == None):
                self.gui_screen.update(game, delta)
    
    def draw(self, ps, game):
        for object in reversed(self.gui_list):
            object.draw(ps, game)
        if not (self.gui_screen == None):
                self.gui_screen.draw(ps, game)
    
    def keyClick(self, game, code):
        if code == sf.Keyboard.E:
            if not (self.gui_screen == None):
                self.gui_screen = None
            else: #PLACE FOR INVENTORY SCREEN
                self.gui_screen = gtscr.GuiTestScreen()
            return False
        return True
    
    
class LoadWorldScreen(Screen):
    
    def __init__(self, game, map = "Random", worldSize = 8):
        self.name = "LOAD_WORLD"
        self.gui_list = []
        self.gui_screen = None
        
        self.step = 0
        self.goalStep = 150
        
        self.map = map
        self.gameMap = 0
        self.physWorld = 0
        self.worldSize = worldSize
        self.tileSize = worldSize * 8
        self.world = 0
        self.player = 0
        self.startPos = sf.Vector2(0,0)
        self.ti = 0
        
        title = GuiText(10,10, "Loading...")
        title.text.character_size = 32
        title.text.style = sf.Text.BOLD
        self.gui_list.append(title)
        
        pegbar = guipb.GuiProgressBas(10, game.window.height - 42, self.goalStep, game.window.width - 20)
        self.bar = pegbar
        self.gui_list.append(pegbar)
        
        self.bar.text.text.string = "Warming up..."
        self.bar.text.text.style = sf.Text.BOLD
        
        self.load_icon = guili.GuiLoadIcon(game, 512, 320)
        self.gui_list.append(self.load_icon)
        
    
    def update(self, game, delta):
        super().update(game, delta)
        
        #WARMING UP...
        if self.step == 1:
            x = 0
        
        #INIT GAME MAP
        if(self.step == 5):
            self.bar.text.text.string = "Init Game Map..."
        
        if(self.step == 6):
            self.gameMap = gmap.GameMap(self.tileSize, self.tileSize)
        
        
        
        #GENERATING/LOAD STUFF
        if(self.step == 10):
            if self.map == "Random":
                self.bar.text.text.string = "Generate Map..."
            else:
                self.bar.text.text.string = "Loading Map..."
        
        if(self.step == 11):
            if self.map == "Random":
                self.gameMap.generate()
            else:
                self.map = ".\\maps\\" + self.map + ".txt"
                self.gameMap.readFromFile(self.map)
        
        #APPLYING STUFF TO THE WORLD
        
        #Making a start and an end...
        if(self.step == 14):
            self.bar.text.text.string = "Making A Start And An End..."
                
        if(self.step == 15):
            if self.map == "Random":
                con = False
                for y in range(self.tileSize):
                    for x in range(self.tileSize):
                        char = self.gameMap.grid[y][x]
                        if char == " ":
                            self.gameMap.grid[y][x] = "H"
                            for y2 in range(-1,2):
                                for x2 in range(-1, 2):
                                    char2 = self.gameMap.grid[y+y2][x+x2]
                                    if char2 == " ":
                                        self.startPos = sf.Vector2((x+x2) * 64, (y+y2) * 64)
                            con = True
                            break
                    if con:
                        break
            else:
                con = False
                for y in range(self.tileSize):
                    for x in range(self.tileSize):
                        char = self.gameMap.grid[y][x]
                        if char == "P":
                            for y2 in range(-1,2):
                                for x2 in range(-1, 2):
                                    char2 = self.gameMap.grid[y+y2][x+x2]
                                    if char2 == " ":
                                        self.startPos = sf.Vector2((x+x2) * 64, (y+y2) * 64)
                            con = True
                            break
                    if con:
                        break
        
        #END OF APPLYING STUFF TO THE WORLD!
        
        #Making An Tile Interpreter...
        if(self.step == 80):
            self.bar.text.text.string = "Making An Tile Interpreter..."
        
        if(self.step == 81):
            self.ti = TileInterpreter(game, self.gameMap)
        
        #Making Things Solid
        if(self.step == 90):
            self.bar.text.text.string = "Making Things Solid..."
        
        if(self.step == 92):
            self.physWorld = PhysWorld(self.ti, self.worldSize)
        
        #Making The World
        if(self.step == 93):
            self.bar.text.text.string = "Making The World..."
        
        if(self.step == 95):
            x = 0
            self.world = GuiWorld(self.physWorld)
        
        #HERE WE WANT TO ADD MONSTERS AND ITEMS!
        
        #Init Player
        if(self.step == 96):
            self.bar.text.text.string = "Playing God..."
        
        if(self.step == 97):
            self.player = PlayerEntity(self.world, 0, 0, game)
            self.world.addEntity(self.player)
            game.player = self.player
        
        #Inserting Player
        if(self.step == 100):
            self.bar.text.text.string = "Climbing In..."
        
        if(self.step == 101):
            self.player.body.rectangle.position = self.startPos
        
        #ADD MORE LOADING STUFF
        
        #STEP HANDLING AND BOOT UP OF PLAY SCREEN
        if self.step <= self.goalStep:
            self.step += 1
            self.bar.currentSteps = self.step
        
        if self.step == self.goalStep:
            game.next = PlayScreen(game, self.physWorld, self.world)
            #self.bar.text.text.string = "DONE!"
        
        
        
        














from gui.gui_world import GuiWorld
from world.cool_phys import PhysWorld, PhysBody
from entity.entity import PlayerEntity
from world.tile_interpreter import TileInterpreter


