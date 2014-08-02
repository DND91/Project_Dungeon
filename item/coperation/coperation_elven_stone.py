#!/usr/bin/python
import item.coperation.coperation as cop

class ElvenStoneCoperation(cop.Coperation):
    def __init__(self):
        self.name = "Elven Stone"
    
    def setupStack(self, stack):
        stack.name = stack.name + " Of " + self.name
