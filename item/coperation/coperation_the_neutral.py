#!/usr/bin/python
import item.coperation.coperation as cop

class TheNeutralCoperation(cop.Coperation):
    def __init__(self):
        self.name = "Neutral"
    
    def setupStack(self, stack):
        stack.name = self.name + " " + stack.name