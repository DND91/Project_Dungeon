#!/usr/bin/python
import random as rnd
import math

class Race:
    def __init__(self):
        self.name = "Standard"
        self.race_points = 50
        self.weights = [1,1,1,1,1]
        
    
    
    
    def getName(self):
        return self.name
    
    def getCost(self):
        return 0
    
    def scrambleBaseStats(self, stats, rate = 20, maxV = 18, minV = 5):
        bases = ["Might", "Vitality", "Quickness", "Mind", "Magic"]
        for x in range(rate):
            high = rnd.choice(bases)
            low = rnd.choice(bases)
            
            if maxV <= stats[high]:
                continue
            if stats[low] <= minV:
                continue
            
            stats[high] += 1
            stats[low] -= 1
    
    def setupBaseStats(self, stats, sp = 50, weights = [1,1,1,1,1]):
        tot = 0
        for x in weights:
            tot += x
        for p in range(len(weights)):
            weights[p] = weights[p] / tot
        
        stats["Might"] = math.floor(sp * weights[0])
        stats["Vitality"] = math.floor(sp * weights[1])
        stats["Quickness"] = math.floor(sp * weights[2])
        stats["Mind"] = math.floor(sp * weights[3])
        stats["Magic"] = math.floor(sp * weights[4])
        self.scrambleBaseStats(stats)
    
    def setup(self, stats):
        self.setupBaseStats(stats, self.race_points, self.weights)
    
    def makePersonality(self, stats):
        stats["Personality"] = "Common"
    
    def makeDraw(self, stats):
        stats["Texture"] = "SOLID"
    


























