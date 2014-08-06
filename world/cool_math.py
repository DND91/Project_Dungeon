#!/usr/bin/python
import sfml as sf
import math

def getDistance(a, b):
        dx = a.x - b.x
        dy = a.y - b.y
        return math.sqrt(math.pow(dx,2) + math.pow(dy,2))

def gap(a, b):
    rectA = a.rectangle
    rectB = b.rectangle
    
    length = rectB.center.x - rectA.center.x
    half_a = rectA.width * 0.5
    half_b = rectB.width * 0.5
    gapX = half_a + half_b - math.fabs(length)
    if length < 0:
        gapX *= -1
    
    length = rectB.center.y - rectA.center.y
    half_a = rectA.height * 0.5
    half_b = rectB.height * 0.5
    gapY = half_a + half_b - math.fabs(length)
    if length < 0:
        gapY *= -1
    
    return sf.Vector2(gapX, gapY)

def intersects(a, b):
    # make sure the rectangle is a rectangle (to get its right/bottom border)
    rectA = a.rectangle
    rectB = b.rectangle

    # compute the intersection boundaries
    left = max(rectB.left, rectA.left)
    top = max(rectB.top, rectA.top)
    right = min(rectB.right, rectA.right)
    bottom = min(rectB.bottom, rectA.bottom)

    # if the intersection is valid (positive non zero area), then
    # there is an intersection
    return left < right and top < bottom

    #Any of the rects are inside the other
def contains(a, b):
    rectA = a.rectangle
    rectB = b.rectangle
    
    big = rectA
    small = rectB
    
    if not (rectA.width < rectB.width and rectA.height < rectB.height):
        if not (rectB.width <= rectA.width and rectB.height <= rectA.height):
            return False
    else:
        big = rectB
        small = rectA
        
    return big.top <= small.top and small.bottom <= big.bottom and big.left <= small.left and small.right <= big.right
