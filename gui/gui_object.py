#!/usr/bin/python
import sfml as sf

class GuiObject:
    def __init__(self, x, y, width, height):
        self.rectangle = sf.Rectangle(sf.Vector2(x, y), sf.Vector2(width, height))
    
    def intersects(self, rectangle):
        # make sure the rectangle is a rectangle (to get its right/bottom border)
        l, t, w, h = rectangle
        rectangle = sf.Rectangle((l, t), (w, h))

        # compute the intersection boundaries
        left = max(self.rectangle.left, rectangle.left)
        top = max(self.rectangle.top, rectangle.top)
        right = min(self.rectangle.right, rectangle.right)
        bottom = min(self.rectangle.bottom, rectangle.bottom)

        # if the intersection is valid (positive non zero area), then
        # there is an intersection
        return left < right and top < bottom
    
    def collision(self, mouseRect):
        return self.intersects(mouseRect)
    
    def update(self, game, delta):
        x = 0
    
    def draw(self, ps, game):
        x = 0