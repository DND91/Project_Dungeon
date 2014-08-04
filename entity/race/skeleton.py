#!/usr/bin/python
import entity.race.race as race

class Skeleton(race.Race):
    def __init__(self):
        self.name = "Skeleton"
        self.race_points = 50 + 2 * self.getCost()
        self.weights = [1,1,3,2,3]
    
    def getCost(self):
        return 5
    
    def makePersonality(self, stats):
        stats["Personality"] = "Mindless"
    
    def makeDraw(self, stats):
        stats["Texture"] = "SKELETON"