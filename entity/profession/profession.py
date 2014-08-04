#!/usr/bin/python
import random as rnd
import math

class Profession:
    def __init__(self):
        self.name = "None"
    
    def getName(self):
        return self.name
    
    def getCost(self):
        return 0
    
    def setup(self, stats):
        x = 0