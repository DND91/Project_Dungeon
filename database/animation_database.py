#!/usr/bin/python
import sfml as sf
import os
import glob
import math

class AnimationConfig:
    def __init__(self):
        self.size = [64,64]
        self.frames = 1
        self.speed = 1
    
    def print(self):
        print("Size", self.size)
        print("Frames", self.frames)
        print("Speed", self.speed)

class Animation:
    def __init__(self, texture, config):
        self.texture = texture
        self.sprite = sf.Sprite(texture)
        self.config = config
    
    def print(self):
        self.config.print()
    
    def draw(self, count, x, y, window):
        s = math.floor(count / self.config.speed)
        c = s % self.config.frames
        self.sprite.position = sf.Vector2(x, y)
        self.sprite.texture_rectangle = sf.Rectangle((c*self.config.size[0], 0), (self.config.size[0], self.config.size[1]))
        window.draw(self.sprite)
        

def getNext(gen):
    try:
        return gen.__next__()
    except StopIteration:
        return None

class AnimationCollection:
    def __init__(self, name):
        self.name = name
        self.database = dict()
        self.path = "./"+name+"/"
        main_path = os.getcwd()
        os.chdir(self.path)
        for file in glob.glob("*.png"):
            self.load(file)
        os.chdir(main_path)
    
    def words(self, fileobj):
        for line in fileobj:
            for word in line.split():
                yield word
    
    def load(self, file_name):
        fp = self.path+file_name
        name = file_name[:-4]
        texture = None
        config = AnimationConfig()
        try:
            texture = sf.Texture.from_file(file_name)
        except IOError:
            print("FAILED TO LOAD '" + file_name + "' ON PATH '" + self.path + "'")
        try:
            file = open(name+".txt")
            wordgen = self.words(file)
            word = getNext(wordgen)
            while not (word == None):
                if word == "SIZE":
                    x = getNext(wordgen)
                    y = getNext(wordgen)
                    x = int(x)
                    y = int(y)
                    config.size[0] = x
                    config.size[1] = y
                elif word == "FRAMES":
                    frames = getNext(wordgen)
                    frames = int(frames)
                    config.frames = frames
                elif word == "SPEED":
                    speed = getNext(wordgen)
                    speed = int(speed)
                    config.speed = speed
                word = getNext(wordgen)
            file.close()
        except IOError:
            print("FAILED TO LOAD CONFIG FOR " + file_name + " ON PATH '" + self.path + "'")
        
        self.database[name.upper()] = Animation(texture, config)
    
    def print(self):
        print("Name", self.name)
        print("Path", self.path)
        for key, value in self.database.items():
            print("Action", key)
            value.print()
    
    def draw(self, action, count, x, y, window):
        self.database[action].draw(count, x, y, window)
    

class AnimationDatabase:
    database = dict()
    
    def __init__(self):
        self.load_all()
    
    def load_all(self):
        main_path = os.getcwd()
        os.chdir("./resources/animation/")
        thedir = os.getcwd()
        
        for dir in os.listdir(thedir):
            self.database[dir.upper()] = AnimationCollection(dir)
        
        
        
        os.chdir(main_path)
    
    def print(self):
        for key, value in self.database.items():
            print("ANIMATION", key)
            value.print()
    
    def draw(self, animation, action, count, x , y, window):
        self.database[animation].draw(action, count, x, y, window)




















