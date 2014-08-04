#!/usr/bin/python
import random as rnd
import math

class Warrior:
    def __init__(self):
        self.name = "Warrior"
    
    def getName(self):
        return self.name
    
    def getCost(self):
        return 4
    
    def setup(self, stats):
        x = 0