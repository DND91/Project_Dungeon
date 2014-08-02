#!/usr/bin/python
import item.coperation.coperation as cop

class ChaosCoperation(cop.Coperation):
    def __init__(self):
        self.name = "Chaos"
    
    def setupStack(self, stack):
        stack.name = self.name + " " + stack.name