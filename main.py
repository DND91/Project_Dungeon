#!/usr/bin/python
from game import *
import sfml as sf
import gui.gui_text as gui_text

def run():
    framerate_limit = 60.0
    game = Game()
    game.window.icon = game.textures.fetch("HORSE").to_image().pixels
    game.window.framerate_limit = framerate_limit
    clock = sf.Clock()
    
    fpsCounter = gui_text.GuiText(5, 0, "FPS: 0")
    fpsCounter.text.color = sf.Color.BLUE
    fps = "FPS: "
    time = framerate_limit
    while game.running:
        delta = clock.elapsed_time.milliseconds
        secs = clock.elapsed_time.seconds
        clock.restart()
        #EVENT
        for event in game.window.events:
            if type(event) is sf.CloseEvent:
                game.window.close()
                game.running = False
            elif type(event) is sf.FocusEvent:
                if event.gained:
                    game.pause = False
                elif event.lost:
                    game.pause = True
            else:
                game.current.event(game, event)
        #UPDATE
        if not game.pause:
            game.current.update(game, delta)
            #UPDATE SCREEN
            if game.next != 0:
                game.current = None
                game.current = game.next
                game.next = 0
                game.current.update(game, delta)
            fpsCounter.update(game, delta)
            #DRAW
            game.window.clear(sf.Color.BLACK)
            for ps in range(6):
                game.current.draw(ps, game)
            time = time * 0.95 + secs * 0.05
            fpsCounter.text.string = (fps + str(round(1.0/time, 1)))
            fpsCounter.draw(0,game)
            game.window.display()
            #sf.system.sleep(sf.seconds(0.1))
    
    game.window.close()
    #exit(1)
    
run()