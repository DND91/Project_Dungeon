#!/usr/bin/python

import random as rnd

coperations = []

def randomCoop(stack):
    cope = rnd.choice(coperations)
    cope.setupStack(stack)

class TheNeutralCoperation:
    def __init__(self):
        self.name = "Neutral"
        coperations.append(self)
    
    def setupStack(self, stack):
        stack.name = self.name + " " + stack.name

class ChaosCoperation(TheNeutralCoperation):
    def __init__(self):
        self.name = "Chaos"
        coperations.append(self)
    
    def setupStack(self, stack):
        stack.name = self.name + " " + stack.name

class ElvenStoneCoperation(TheNeutralCoperation):
    def __init__(self):
        self.name = "Elven Stone"
        coperations.append(self)
    
    def setupStack(self, stack):
        stack.name = stack.name + " Of " + self.name



























#COPERATIONS
TheNeutralCoperation()
ChaosCoperation()
ElvenStoneCoperation()



