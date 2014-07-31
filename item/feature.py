#!/usr/bin/python

features = dict()

class Feature:
    
    def __init__(self, name, cost, parts):
        self.name = name
        self.cost = cost
        self.parts = parts
        for part in parts:
            if not (part in features):
                features[part] = []
            features[part].append(self)
    
    def __str__(self):
        return "Feature." + self.name + "(" + str(self.cost) +")"
    
    def __repr__(self):
        return self.__str__()
    
    def description(self, part):
        return self.name + " " + part



snake = Feature("Snake", 0, ["Decor"])
appel = Feature("Snake", 4, ["Decor"])
stone = Feature("Stone", 0, ["Base", "Chain", "Lock"])
copper = Feature("Copper", 2, ["Base", "Chain", "Lock"])
silver = Feature("Silver", 4, ["Base", "Chain", "Lock"])
gold = Feature("Gold", 6, ["Base", "Chain", "Lock"])

wool = Feature("Wool", 2, ["Cloth", "Hood"])
spider_silk = Feature("Spider Silk", 10, ["Cloth", "Hood"])
rags = Feature("Rags", 0, ["Cloth", "Hood"])





























