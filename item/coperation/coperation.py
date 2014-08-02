#!/usr/bin/python

class Coperation:
    def __init__(self):
        self.name = "COPERATION"
    
    def setupStack(self, stack):
        stack.name = self.name + " " + stack.name

