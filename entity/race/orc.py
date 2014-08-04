#!/usr/bin/python
import entity.race.race as race

class Orc(race.Race):
    def __init__(self):
        self.name = "Orc"
        self.race_points = 50 + 2 * self.getCost()
        self.weights = [3,3,2,1,1]
    
    def getCost(self):
        return 3
    
    def makePersonality(self, stats):
        stats["Personality"] = "Brutal"
    
    def makeDraw(self, stats):
        stats["Texture"] = "ORC"
