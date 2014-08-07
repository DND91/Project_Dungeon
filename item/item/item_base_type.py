class ItemBaseType:

    def __init__(self, name, occurence, cost, **kwargs):
        
        self._name = name
        self._occurence = occurence
        self._cost = cost
        self.stats = kwargs

    @property
    def occurence(self):
        return self._occurence

    @property
    def cost(self):
        return self._cost

    @property
    def name(self):
        return self._name
