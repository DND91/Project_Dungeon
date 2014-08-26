#!/usr/bin/python
import sfml as sf
import os
import glob

class Animation:
    def __init__(self, name):
        self.name = name
        self.database = dict()
        self.path = "./"+name+"/"
        main_path = os.getcwd()
        os.chdir(self.path)
        for file in glob.glob("*.png"):
            fp = self.path+file
            action = file[:-4]
            try:
                texture = sf.Texture.from_file(file)
                self.database[action.upper()] = texture
            except IOError:
                print("FAILED TO LOAD '" + file + "' ON PATH '" + fp + "'")
        os.chdir(main_path)
        
    def print(self):
        print(self.name)
        print(self.path)
        for key, value in self.database.items():
            print(key)
    

class AnimationDatabase:
    database = dict()
    
    def __init__(self):
        self.load_all()
    
    def load_all(self):
        main_path = os.getcwd()
        os.chdir("./resources/animation/")
        thedir = os.getcwd()
        
        for dir in os.listdir(thedir):
            self.database[dir.upper()] = Animation(dir)
        
        
        
        os.chdir(main_path)
    
    def print(self):
        for key, value in self.database.items():
            print(key)
            value.print()




















