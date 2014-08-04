#!/usr/bin/python
import random as rnd
import math

class Hunter:
    def __init__(self):
        self.name = "Hunter"
    
    def getName(self):
        return self.name
    
    def getCost(self):
        return 2
    
    def setup(self, stats):
        x = 0