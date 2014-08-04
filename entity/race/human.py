#!/usr/bin/python
import entity.race.race as race

class Human(race.Race):
    def __init__(self):
        self.name = "Human"
        self.race_points = 50
        self.weights = [1,1,1,1,1]
    
    def makePersonality(self, stats):
        stats["Personality"] = "Common"
    
    def makeDraw(self, stats):
        stats["Texture"] = "HUMAN"